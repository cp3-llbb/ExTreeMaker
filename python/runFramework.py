__author__ = 'sbrochet'

from pytree import Tree
from Core.AnalysisEvent import AnalysisEvent
from Core.ProductManager import ProductManager

import os
import time
import itertools
from optparse import OptionParser

usage = """%prog [options]"""
description = """Launch the framework to produce a nice tree."""
epilog = """Example:
./runFramework.py -i ./ -o output.root -c TestConfiguration
"""
parser = OptionParser(usage=usage, add_help_option=True, description=description, epilog=epilog)
parser.add_option("-c", "--configuration", dest="conf", default=None,
                  help="Analyzer class.")
parser.add_option("-i", "--inputPath", dest="path",
                  help="Read input file from DIR.", metavar="DIR")
parser.add_option("-o", "--output", dest='outputname', default=None,
                  help="Save output as FILE.", metavar="FILE")
parser.add_option("--all", action="store_true", dest="all",
                  help="Process all levels.")
parser.add_option("-l", "--level", dest="levels",
                  help="Specify a coma-separated list of levels to be processed. No space is allowed.")
parser.add_option("--Njobs", type="int", dest='Njobs', default="1",
                  help="Number of jobs when splitting the processing.")
parser.add_option("--jobNumber", type="int", dest='jobNumber', default="0",
                  help="Number of the job is a splitted set of jobs.")
parser.add_option("--nEvents", type="int", dest='nEvents', default="0",
                  help="Run only nEvents for the given job. Useful for testing")

(options, args) = parser.parse_args()

if options.conf is None:
    raise RuntimeError("You must provide a configuration file")

# Load configuration class

configurationClass = os.path.splitext(options.conf)[0]
configurationModule = __import__(configurationClass)

configuration = getattr(configurationModule, configurationClass)()

def runAnalysis(input_files, output_name, Njobs=1, jobNumber=1):
    """
    Main function. Loop over all events and call what's need to be called

    :param input_files: The input file or directory
    :param output_name: The output filename
    :param Njobs: Number of total jobs
    :param jobNumber: Index of the current job
    :return: Nothing
    """

    # inputs
    files = []
    if os.path.isdir(input_files):
        dirList = list(itertools.islice(os.listdir(input_files), jobNumber, None, Njobs))
        for fname in dirList:
            files.append(os.path.join(input_files, fname))
    elif os.path.isfile(input_files):
        files = [input_files]
    else:
        files = []

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
    events = AnalysisEvent(files)

    # Register collections
    for collection in collections:
        events.addCollection(collection.name, collection.type, collection.input_tag)

    # Call beginJob
    for runnable in runnables:
        runnable.beginJob()

    # main event loop
    i = 0
    events_saved = 0
    t0 = time.time()
    for event in events:
        # printout
        if i % 100 == 0:
            print "Processing... event %d. Last batch in %f s." % (i, (time.time() - t0))
            t0 = time.time()
        if i >= options.nEvents != 0:
            break

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
            else:
                tree.reset_branch_values()

        else:
            tree.Fill(reset=True)
            events_saved += 1

        if events_saved == 1:
            # Freeze all the products
            product_manager._frozen = True

        for category in analyzer._categories.itervalues():
            category.reset()
            for cut in category.cuts.itervalues():
                cut.model.reset()

        i += 1

    # Call endJob
    for runnable in runnables:
        runnable.endJob()

    # Write the tree
    output.Write()

    # close the file
    output.Close()

    print('')
    print('Job done. %d events processed, %d events saved' % (i, events_saved))
    if len(events_saved_per_category) > 0:
        print('{:60s} {:20s}'.format('Category', '# events'))
        print('-' * 81)
        for name, value in events_saved_per_category.items():
            print('{:60s} {:<20d}'.format(name, value))


runAnalysis(input_files=options.path, output_name=options.outputname, Njobs=options.Njobs, jobNumber=options.jobNumber)