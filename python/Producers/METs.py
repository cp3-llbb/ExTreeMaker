__author__ = 'obondu'

import Models.METs
from Producer import Producer
from Producers.Helper import fill_candidate

class METs(Producer):

    def __init__(self, name, prefix, met_collection):
        Producer.__init__(self, name)

        self.uses(name, 'std::vector<pat::MET>', met_collection)
        self.produces(Models.METs.METs, name, prefix)

    def produce(self, event, products):
        mets = getattr(event, self._name)
        product = getattr(products, self._name)
        for met in mets:
            fill_candidate(met, product)