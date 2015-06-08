__author__ = 'sbrochet'

import os
import re

from Core.Binning import OneDimensionBinning

def file_lookup(paths, f):
    """
    Iterates over 'paths' and look if a file named 'f' exists
    :param paths: An array of absolute paths
    :param f: A relative file name
    :return: The absolute path of 'f' if found in 'paths', None otherwise
    """

    for path in paths:
        if os.path.exists(os.path.join(path, f)):
            return os.path.join(path, f)

    return None

effective_areas_line_regex = re.compile("^\s*([-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?)"
                                        "\s*([-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?)"
                                        "\s*([-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?)\s*$")

def parse_effective_areas_file(f):
    """
    Parse the text file 'f' containing effective area values.
    :param f: The relative path of the text file. The absolute path of this file is searched in $CMSSW_SEARCH_PATH
    :return: An instance of :class:`OneDimensionBinning` class filled with values red from the file
    """
    paths = os.environ['CMSSW_SEARCH_PATH'].split(os.pathsep)
    absolute_file = file_lookup(paths, f)
    if absolute_file is None:
        raise IOError("File %r not found. Lookup paths: %s" % (f, paths))

    binning = OneDimensionBinning()
    with open(absolute_file) as _f:
        content = _f.readlines()
        for line in content:
            line = line.strip()
            if line.startswith('#'):
                continue
            m = effective_areas_line_regex.match(line)
            if m is None:
                continue

            binning.add(float(m.group(1)), float(m.group(2)), float(m.group(3)))

    return binning
