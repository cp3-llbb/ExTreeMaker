__author__ = 'sbrochet'

"""
Main entry point of the framework. This file is loaded either by runFramework from this package or
runFrameworkOnGrid from the GridIn package
"""

from pytree import Tree
from Core.AnalysisEvent import AnalysisEvent
from Core.ProductManager import ProductManager
from Core.ReportProducer import ReportProducer
from Core.LumiMask import LumiMask

import os
import time
import signal

def sigint_handler(signal, frame):
        global global_interrupt
        global_interrupt = True

def run(configuration_file, input_files, output_name, n_events, report_file_name=None, lumi_mask=None):
    """
    Main function. Loop over all events and call what's need to be called

    :param input_files: A list of input files
    :param output_name: The output filename
    :param n_events: Maximum number of events to process. -1 for all
    :return: Nothing
    """

    # Register CTRL+C handler to exit gracefully
    global global_interrupt
    global_interrupt = False
    signal.signal(signal.SIGINT, sigint_handler)

    configurationClass = os.path.splitext(configuration_file)[0]
    configurationModule = __import__(configurationClass)

    configuration = getattr(configurationModule, configurationClass)()

    # Parse configuration
    if output_name is None:
        output_name = configuration.output_file

    # Instantiate analysis
    analyzer = configuration.analyzer(**configuration.analyzer_configuration)

    # Build producers
    producers = []
    for producer in configuration.producers:
        clazz = producer.clazz
        del producer.clazz
        p = clazz(**producer.__dict__)
        producers.append(p)

    import ROOT

    # output
    output = ROOT.TFile.Open(output_name, "RECREATE")

    # output tree
    tree = Tree(configuration.tree_name)

    # Collect runnables
    runnables = producers + [analyzer]

    # Collect collections
    collections = configuration.collections
    for runnable in runnables:
        collections.extend(runnable._collections)

    # Create branches
    def createBranches(products):
        for product in products:
            tree.set_buffer(product['instance'], create_branches=True)

    for runnable in runnables:
        createBranches(runnable._products)

    # Create branches in the tree for each registered cut of the analyzer
    # Store description as a 'user info' list into the tree

    categories_info = ROOT.TObjArray()
    categories_info.SetName('categories')

    cuts_info = ROOT.TObjArray()
    cuts_info.SetName('cuts')

    events_saved_per_category = {}
    for cat_name, category in analyzer._categories.items():
        categories_info.Add(ROOT.TObjString('%s:%s' % (category.name, category.description)))
        tree.set_buffer(category.model, create_branches=True, visible=False)
        category.register_cuts()
        events_saved_per_category[category.description] = 0

        for cut_name, cut in category.cuts.items():
            cuts_info.Add(ROOT.TObjString('%s:%s:%s' % (category.name, cut.name, cut.description)))
            tree.set_buffer(cut.model, create_branches=True, visible=False)

    tree.GetUserInfo().Add(categories_info)
    tree.GetUserInfo().Add(cuts_info)

    # Products manager. Main access point to products from Analyzer
    product_manager = ProductManager(tree, [product for x in runnables for product in x._products])

    # events iterator, plus configuration of standard collections and producers
    events = AnalysisEvent(input_files)

    # Register collections
    for collection in collections:
        events.addCollection(collection.name, collection.type, collection.input_tag)

    # Call beginJob
    for runnable in runnables:
        runnable.beginJob()

    # Job report
    job_report = None
    if report_file_name is not None:
        job_report = ReportProducer(report_file_name)
        job_report.report_output_file(os.path.abspath(output_name))

    # Lumi mask
    if lumi_mask is not None:
        lumi_mask = LumiMask(lumi_mask)

    # main event loop
    i = 0
    events_saved = 0
    t0 = time.time()
    old_current_file = None
    current_file_token = None
    old_run = None
    old_lumi = None

    for event in events:

        if global_interrupt:
            break

        # printout
        if i % 100 == 0:
            print "Processing... event %d. Last batch in %f s." % (i, (time.time() - t0))
            t0 = time.time()
        if 0 < n_events <= i:
            break

        i += 1

        run = event.run()
        lumi = event.lumi()

        if job_report is not None:
            current_file = event.get_current_file().GetName()

            if current_file != old_current_file:
                old_run = None
                old_lumi = None
                old_current_file = current_file
                current_file_token = job_report.report_input_file(current_file)

            job_report.report_event_read(current_file_token)

        if lumi_mask and (run, lumi) not in lumi_mask:
            continue

        if job_report is not None and (run != old_run or lumi != old_lumi):
            job_report.report_lumi_section(current_file_token, run, lumi)
            old_run = run
            old_lumi = lumi

        for producer in producers:
            producer.produce(event, product_manager)

        analyzer.analyze(event, product_manager)

        # Test categories
        for category in analyzer._categories.itervalues():
            if category._test_event_category(product_manager):
                category._evaluate_cuts(product_manager)

        # To be kept, an event must belong to at least one category
        if len(analyzer._categories) > 0:
            keepEvent = False
            for category_name, category in analyzer._categories.items():
                if category.in_category:
                    keepEvent |= True
                    events_saved_per_category[category.description] += 1

            if keepEvent:
                tree.Fill(reset=True)
                events_saved += 1
                if job_report is not None:
                    job_report.report_event_saved()
            else:
                tree.reset_branch_values()

        else:
            tree.Fill(reset=True)
            events_saved += 1
            if job_report is not None:
                job_report.report_event_saved()

        if events_saved == 1:
            # Freeze all the products
            product_manager._frozen = True

        for category in analyzer._categories.itervalues():
            category.reset()
            for cut in category.cuts.itervalues():
                cut.model.reset()

    # Call endJob
    for runnable in runnables:
        runnable.endJob()

    # Write the tree
    output.Write("dummy", ROOT.TObject.kOverwrite)

    # close the file
    output.Close()

    # Report
    if job_report is not None:
        job_report.save()
        print('Job report saved as %r' % report_file_name)

    print('')
    print('Job done. %d events processed, %d events saved' % (i, events_saved))
    if len(events_saved_per_category) > 0:
        print('{:60s} {:20s}'.format('Category', '# events'))
        print('-' * 81)
        for name, value in events_saved_per_category.items():
            print('{:60s} {:<20d}'.format(name, value))
