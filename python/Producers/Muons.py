__author__ = 'obondu'

import Models.Muons
from Producer import Producer
from ROOT.Math import LorentzVector

class Muons(Producer):

    def __init__(self, name, muon_collection):
        Producer.__init__(self, name)

        self.uses('muons', 'std::vector<pat::Muon>', muon_collection)
        self.produces(Models.Muons.Muons, 'muons', 'muon_')

    def produce(self, event, products):
        for muon in event.muons:
            p4 = LorentzVector('ROOT::Math::PtEtaPhiE4D<float>')(muon.pt(), muon.eta(), muon.phi(), muon.energy())
            products.muons.muon_p4.push_back(p4)
            products.muons.muon_isLooseMuon.push_back(True)
