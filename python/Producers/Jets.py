__author__ = 'sbrochet'

import Models.Jets
import random
from Producer import Producer
from ROOT.Math import LorentzVector

class Jets(Producer):

    def __init__(self, name, jet_collection):
        Producer.__init__(self, name)

        self.uses('jets', 'std::vector<pat::Jet>', jet_collection)
        self.produces(Models.Jets.Jets, 'jets', 'jet_')

    def produce(self, event, products):
        for jet in event.jets:
            p4 = LorentzVector('ROOT::Math::PtEtaPhiE4D<float>')(jet.pt(), jet.eta(), jet.phi(), jet.energy())
            products.jets.jet_p4.push_back(p4)

            products.jets.pu_jet_id.push_back(random.random())
