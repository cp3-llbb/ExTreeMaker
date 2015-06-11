__author__ = 'sbrochet'

from Core.Runnable import Runnable

class Analyzer(Runnable):
    """The base class of all user-defined analyzers"""

    def __init__(self, **kwargs):
        Runnable.__init__(self)

    def analyze(self, event, products):
        """
        Main function of the analyzer. Called for each event.
        :param event: The current event
        :param products: an instance of :class:`Core.ProductManager``. You can access from it all the products produced
                by others producers
        :return:
        """
        raise NotImplementedError()
