__author__ = 'obondu'

import Models.METs
from Producer import Producer
from ROOT.Math import LorentzVector

class METs(Producer):

    def __init__(self, name, met_collection):
        Producer.__init__(self, name)

        self.uses('mets', 'std::vector<pat::MET>', met_collection)
        self.produces(Models.METs.METs, 'mets', 'mets_')

    def produce(self, event, products):
        for met in event.mets:
            p4 = LorentzVector('ROOT::Math::PtEtaPhiE4D<float>')(met.pt(), met.eta(), met.phi(), met.energy())
            products.mets.mets_p4.push_back(p4)