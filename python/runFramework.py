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
        alias = producer.alias
        del producer.clazz
        del producer.alias
        p = clazz(alias, **producer.__dict__)
        producers.append(p)

    for producer in analyzer._producers:
        exists = next((x for x in producers if isinstance(x, type(producer)) and x._name == producer._name), None) is \
            not None
        if exists:
            print("A %r producer named %r already exists. Skipping." % (producer.__class__.__name__, producer._name))
            continue

        producers.append(producer)


    import ROOT

    # output
    output = ROOT.TFile.Open(output_name, "RECREATE")

    # output tree
    tree = Tree(configuration.tree_name)

    # Collect runnables
    runnables = producers + [analyzer]

    # Collect collections
    collections = []
    for collection in configuration.collections:
        c = {'name': collection.alias, 'type': collection.type, 'input_tag': collection.input_tag}
        collections.append(c)

    for runnable in runnables:
        collections.extend(runnable._collections)

    # Create branches
    def createBranches(products):
        for product in products:
            tree.set_buffer(product['instance'], create_branches=True)

    for runnable in runnables:
        createBranches(runnable._products)

    # Products manager. Main access point to products from Analyzer
    product_manager = ProductManager([product for x in runnables for product in x._products])

    # events iterator, plus configuration of standard collections and producers
    events = AnalysisEvent(files)

    # FIXME: Work on selections
    #EventSelection.prepareAnalysisEvent(events)

    # Register collections
    for collection in collections:
        events.addCollection(collection['name'], collection['type'], collection['input_tag'])

    # Call beginJob
    for runnable in runnables:
        runnable.beginJob()

    # main event loop
    i = 0
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

        # fill the tree
        tree.Fill(reset=True)

        i += 1

    # Call endJob
    for runnable in runnables:
        runnable.endJob()

    # Write the tree
    output.Write()

    # close the file
    output.Close()


runAnalysis(input_files=options.path, output_name=options.outputname, Njobs=options.Njobs, jobNumber=options.jobNumber)