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

def get_categories(tree):
    """
    Read from the tree the list of cuts applied.
    :param tree: The tree produced by the framework
    :return: A nested dictionary where the key is the category name, and the value is another dictionary. For this one,
    the key 'description' is the category description, and the key 'cuts' is a dictionary where cut name is the key and
    cut description the value.
    """

    treeCategories = tree.GetUserInfo().FindObject('categories')
    if not treeCategories:
        return {}

    categories = {}
    for category in treeCategories:
        category = str(category.GetString())
        name, description = category.split(':', 2)
        categories[name] = {'description': description, 'cuts': {}}

    treeCuts = tree.GetUserInfo().FindObject('cuts')
    if not treeCuts:
        return categories

    for cut in treeCuts:
        # format of cut should be '<category_name>:<name>:<description>'
        cut = str(cut.GetString())
        category_name, name, description = cut.split(':', 3)
        categories[category_name]['cuts'][name] = description

    return categories
