__author__ = 'sbrochet'

from Core.Runnable import Runnable

class Producer(Runnable):

    def __init__(self, name):
        Runnable.__init__(self)

        self._name = name

    def produce(self, event, products):
        raise NotImplementedError()