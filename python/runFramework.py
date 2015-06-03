__author__ = 'sbrochet'

from pytree import Tree
from Core.AnalysisEvent import AnalysisEvent

import os
import time
import itertools
from optparse import OptionParser

usage = """%prog [options]"""
description = """Launch the framework to produce a nice tree."""
epilog = """Example:
./runFramework.py -i ./ -o output.root -a TestAnalyzer
"""
parser = OptionParser(usage=usage, add_help_option=True, description=description, epilog=epilog)
parser.add_option("-a", "--analyzer", dest="analyzer", default=None,
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

if options.analyzer is None:
    raise RuntimeError("You must provide an analyzer class")

if options.outputname is None:
    options.outputname = "output_mc.root"

# Load analyzer class

analyzerClass = os.path.splitext(options.analyzer)[0]
analyzerModule = __import__(analyzerClass)

analyzer = getattr(analyzerModule, analyzerClass)()

def runAnalysis(input, outputname="output_mc.root", Njobs=1, jobNumber=1):
    """
    Main function. Loop over all events and call what's need to be called

    :param input: The input file or directory
    :param outputname: The output filename
    :param Njobs: Number of total jobs
    :param jobNumber: Index of the current job
    :return: Nothing
    """

    # inputs
    files = []
    if os.path.isdir(input):
        dirList = list(itertools.islice(os.listdir(input), jobNumber, None, Njobs))
        for fname in dirList:
            files.append(os.path.join(input, fname))
    elif os.path.isfile(input):
        files = [input]
    else:
        files = []

    import ROOT

    # output
    output = ROOT.TFile.Open(outputname, "RECREATE")

    # output tree
    tree = Tree('tree')

    # Collect runnables
    runnables = analyzer._producers + [analyzer]

    # Create branches
    def createBranches(products):
        for product in products:
            tree.set_buffer(product, create_branches=True)

    for runnable in runnables:
        createBranches(runnable._products)

    # events iterator, plus configuration of standard collections and producers
    events = AnalysisEvent(files)

    # FIXME: Work on selections
    #EventSelection.prepareAnalysisEvent(events)

    # Register collections
    def registerCollections(collections):
        for collection in collections:
            events.addCollection(collection['name'], collection['type'], collection['inputTag'])

    for runnable in runnables:
        registerCollections(runnable._collections)

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

        for producer in analyzer._producers:
            producer.produce(event)

        analyzer.analyze(event)

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


runAnalysis(input=options.path, outputname=options.outputname, Njobs=options.Njobs, jobNumber=options.jobNumber)
