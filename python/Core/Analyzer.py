__author__ = 'sbrochet'

from Core.Runnable import Runnable

class Analyzer(Runnable):
    """The base class of all user-defined analyzers"""

    def __init__(self, **kwargs):
        Runnable.__init__(self)
        self._producers = []

    def analyze(self, event, products):
        """
        Main function of the analyzer. Called for each event.
        :param event: The current event
        :param products: an instance of :class:`Core.ProductManager``. You can access from it all the products produced
                by others producers
        :return:
        """
        raise NotImplementedError()

    def runs(self, clazz, name):
        """
        Inform the framework to run the producer clazz before the analyzer
        :param clazz: The class name of the Producer
        :param name: The name of the Producer. Tree branches will be prefixed by this name
        :return:
        """

        producer = clazz(name=name)

        self._producers.append(producer)
