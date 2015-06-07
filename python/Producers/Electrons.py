__author__ = 'obondu'

import Models.Electrons
from Producer import Producer
from ROOT.Math import LorentzVector

class Electrons(Producer):

    def __init__(self, name, electron_collection):
        Producer.__init__(self, name)

        self.uses('electrons', 'std::vector<pat::Electron>', electron_collection)
        self.produces(Models.Electrons.Electrons, 'electrons', 'electron_')

    def produce(self, event, products):
        for electron in event.electrons:
            p4 = LorentzVector('ROOT::Math::PtEtaPhiE4D<float>')(electron.pt(), electron.eta(), electron.phi(), electron.energy())
            products.electrons.electron_p4.push_back(p4)
            products.electrons.electron_isLooseElectron.push_back(True) # fixme: implement ID criteria
            products.electrons.electron_isTightElectron.push_back(True)
