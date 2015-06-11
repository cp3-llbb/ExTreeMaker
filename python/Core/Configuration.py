__author__ = 'sbrochet'

from collections import namedtuple

class Producer:
    def __init__(self, name, clazz, prefix, **kwds):
        self.name = name
        self.clazz = clazz
        self.prefix = prefix
        self.__dict__.update(kwds)

    def clone(self, **kwargs):
        params = self.__dict__.copy()
        params.update(kwargs)

        return self.__class__(**params)

    def __str__(self):
        return 'Producer %r:%r -> %r' % (self.name, self.prefix, self.clazz)

Collection = namedtuple('Collection', 'name type input_tag')

class Configuration:

    """
    The class name of the analyzer you want to run. Must be specified
    """
    analyzer = None

    """
    The name of the output file produced by the framework. Can be overridden when launching runFramework.py
    """
    output_file = 'output_mc.root'

    """
    The name of the output tree
    """
    tree_name = 'tree'

    """
    List of producers you want to run before your analyzer. Products produced by these producers will be stored
    inside the output file tree.

    The framework expect each value of the list to be an instance of :class:`Bunch` with at least the fields
    ``clazz`` and ``alias`` set.
    """
    producers = []

    """
    List of collections your analyzer depends on.

    The framework expect each value of this list to be an instance of :class:`Collection`
    """
    collections = []

    analyzer_configuration = {}
