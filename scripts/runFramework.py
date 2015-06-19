#! /usr/bin/env python

__author__ = 'sbrochet'

import sys
import os
sys.path.insert(1, '.')

python_path = os.path.join(os.environ['CMSSW_BASE'], 'src/cp3_llbb/ExTreeMaker/python')
if python_path not in sys.path:
    sys.path.insert(1, python_path)

import Framework

from optparse import OptionParser

def parse_input(input):
    """
    Parse input and returns a list of input file
    :param input: Can be a list of files, a path, a .list file or a DAS dataset
    :return: A list of absolute path
    """
    files = []
    if os.path.isdir(input):
        files = [os.path.join(input, x) for x in os.listdir(input) if os.path.splitext(x)[1] == '.root']
    elif os.path.isfile(input):
        extension = os.path.splitext(input)[1]
        if extension == '.list':
            # Read the list of files from the list file
            with open(input) as f:
                files = [x.strip() for x in f.readlines() if not x.strip().startswith('#')]
        else:
            files = [input]
    elif isinstance(input, str) and input.startswith('/'):
        # DAS dataset
        print('Doing DAS query for dataset %r' % input)
        from cp3_llbb.ExTreeMaker import das_client
        query = 'file dataset=%s' % input
        result = das_client.get_data('https://cmsweb.cern.ch', query, 0, 0, 0)
        for data in result['data']:
            files += ['root://xrootd-cms.infn.it/%s' % x['name'].encode('ascii','ignore')
                      for x in data['file'] if 'dataset' in x]
        pass
    elif isinstance(input, str) and input.startswith('root://'):
        files = [input]
    else:
        raise NameError('Invalid input: %r' % input)

    return files

def get_options():
    usage = """%prog [options]"""
    description = """Launch the framework to produce a nice tree."""
    epilog = """Example:
    ./runFramework.py -i ./ -o output.root -c TestConfiguration
    """
    parser = OptionParser(usage=usage, add_help_option=True, description=description, epilog=epilog)
    parser.add_option("-c", "--configuration", dest="conf", default=None,
                      help="Analyzer class.")
    parser.add_option("-i", "--input", dest="input", help="Input file. Can be a ROOT file, a folder, a .list file"
                                                          "or a DAS dataset", metavar="DIR")
    parser.add_option("-o", "--output", dest='outputname', default=None,
                      help="Save output as FILE.", metavar="FILE")
    parser.add_option("--Njobs", type="int", dest='Njobs', default="1",
                      help="Number of jobs when splitting the processing.")
    parser.add_option("--jobNumber", type="int", dest='jobNumber', default="0",
                      help="Number of the job is a splitted set of jobs.")
    parser.add_option("--nEvents", type="int", dest='nEvents', default="-1",
                      help="Run only nEvents for the given job. Useful for testing")

    (options, args) = parser.parse_args()

    if options.conf is None:
        raise RuntimeError("You must provide a configuration file")

    return options

options = get_options()
Framework.run(options.conf, input_files=parse_input(options.input), output_name=options.outputname,
              n_events=options.nEvents)
