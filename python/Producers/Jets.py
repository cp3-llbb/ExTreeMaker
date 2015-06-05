__author__ = 'sbrochet'

import Models.Jets
from Producer import Producer

from Helper import fill_candidate

class Jets(Producer):

    def __init__(self, name, prefix, jet_collection):
        Producer.__init__(self, name)

        self.uses(name, 'std::vector<pat::Jet>', jet_collection)
        self.produces(Models.Jets.Jets, name, prefix)

    def produce(self, event, products):
        jets = getattr(event, self._name)
        product = getattr(products, self._name)
        for jet in jets:
            fill_candidate(jet, product)

            if jet.hasUserFloat('pileupJetId:fullDiscriminant'):
                product.pu_jet_id.push_back(jet.userFloat('pileupJetId:fullDiscriminant'))
