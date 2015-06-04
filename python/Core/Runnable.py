__author__ = 'sbrochet'

from pytree import TreeModel

class Runnable:
    """Base class for Analyzers and Producers"""

    def __init__(self):
        self._collections = []
        self._products = []

    def beginJob(self):
        """
        Called before the event loop
        :return:
        """
        pass

    def endJob(self):
        """
        Called after the event loop
        :return:
        """
        pass

    def uses(self, name, type, inputTag):
        """
        Tell the framework to that the collection inputTag will be used by this analyzer
        :param name: The name of the collection. The collection will be accessible via the event interface using this name
        :param type: The C++ class name of the collection
        :param inputTag: The edm::InputTag of the collection
        :return:
        """
        self._collections.append({'name': name, 'type': type, 'input_tag': inputTag})

    def produces(self, clazz, name, prefix):
        """
        Informs the framework that the analyzer will produce an object of type clazz.
        :param clazz: The class of the object produced by this analyzer. Must derived from Model
        :param name: The name of this object. Set as an attribute of the global ``products`` objects
        :param prefix: Tree branches will be prefixed by this value
        :return:
        """

        if not issubclass(clazz, TreeModel):
            raise TypeError()

        instance = clazz.prefix(prefix)()

        self._products.append({'name': name, 'prefix': prefix, 'instance': instance})
