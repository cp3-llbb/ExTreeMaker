__author__ = 'sbrochet'

from Producer import Producer

import Models.Jets

from ROOT.Math import LorentzVector

class Jets(Producer):

    def __init__(self, name):
        Producer.__init__(self, name)

        self.uses('jets', 'std::vector<pat::Jet>', 'slimmedJets')
        self.jets = self.produces(Models.Jets.Jets, 'jet_')

    def produce(self, event):

        for jet in event.jets:

            p4 = LorentzVector('ROOT::Math::PtEtaPhiE4D<float>')(jet.pt(), jet.eta(), jet.phi(), jet.energy())
            self.jets.jet_p4.push_back(p4)
