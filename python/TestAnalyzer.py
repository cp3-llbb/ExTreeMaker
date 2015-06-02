__author__ = 'sbrochet'

from Core.Analyzer import Analyzer
from Models.Candidates import Candidates

from Producers.Jets import Jets

from ROOT.Math import LorentzVector

class TestAnalyzer(Analyzer):
    def __init__(self):
        Analyzer.__init__(self)

        self.runs(Jets, "jets_")

        self.z = self.produces(Candidates, 'z_candidate_')

    def beginJob(self):
        print("Begin job!")
        pass

    def analyze(self, event):
        print("Analyzing event!")

        p4 = event.jets[0].p4() + event.jets[1].p4()

        self.z.z_candidate_p4.push_back(LorentzVector('ROOT::Math::PtEtaPhiE4D<float>')(p4.Pt(), p4.Eta(), p4.Phi(), p4.E()))

        pass

    def endJob(self):
        print("End job!")
