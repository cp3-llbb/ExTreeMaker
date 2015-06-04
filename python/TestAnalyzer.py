__author__ = 'sbrochet'

from Core.Analyzer import Analyzer
from Models.Candidates import Candidates

from ROOT.Math import LorentzVector

class TestAnalyzer(Analyzer):
    def __init__(self, **kwargs):
        Analyzer.__init__(self)

        self.z = self.produces(Candidates, 'z', 'z_candidate_')

        # Since Jets producer already registers this collection, 'jet' will be set as an alias of 'jets'
        self.uses('vertex', 'std::vector<reco::Vertex>', kwargs['vertex_collection'])
        self.uses('jet', 'std::vector<pat::Jet>', kwargs['jet_collection'])
        self.uses('muon', 'std::vector<pat::Muon>', kwargs['muon_collection'])

    def beginJob(self):
        print("Begin job!")
        pass

    def analyze(self, event, products):
        print("Analyzing event!")

        if len(event.muon) >= 2:
            p4 = event.muon[0].p4() + event.muon[1].p4()
            products.z.p4.push_back(LorentzVector('ROOT::Math::PtEtaPhiE4D<float>')(p4.Pt(), p4.Eta(), p4.Phi(), p4.E()))

        # Access product produced by the Jets producer
        for z in products.z.p4:
            print "Z candidate mass:", z.M()
        print products.jets.pu_jet_id[0]

    def endJob(self):
        print("End job!")
