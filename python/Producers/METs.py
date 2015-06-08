__author__ = 'obondu'

import Models.METs
from Producer import Producer
from Producers.Helper import fill_candidate

class METs(Producer):

    def __init__(self, name, met_collection):
        Producer.__init__(self, name)

        self.uses('mets', 'std::vector<pat::MET>', met_collection)
        self.produces(Models.METs.METs, 'mets', 'mets_')

    def produce(self, event, products):
        for met in event.mets:
            fill_candidate(met, products.mets)