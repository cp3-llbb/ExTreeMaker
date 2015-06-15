__author__ = 'sbrochet'

from Core.Analyzer import Analyzer, Category
from Models.Candidates import Candidates

from ROOT.Math import LorentzVector

class TestAnalyzer(Analyzer):
    class TwoMuonsCategory(Category):
        def register_cuts(self):
            self.new_cut('z_mass', 'Z mass > 5 GeV')
            self.new_cut('leading_muon_pt', 'Leading muon pT > 10 GeV', 'muons.p4[0].Pt() > 10')
            self.new_cut('leading_jet_pt', 'Leading jet pT > 10 GeV')

        def event_in_category(self, products):
            return len(products.muons.p4) > 1

        def evaluate_cuts(self, products):
            if products.z.p4[0].M() > 5:
                self.pass_cut('z_mass')

            if products.jets.p4[0].Pt() > 10:
                self.pass_cut('leading_jet_pt')

    class TwoElectronsCategory(Category):
        def register_cuts(self):
            self.new_cut('z_mass', 'Z mass > 5 GeV')

        def event_in_category(self, products):
            return len(products.electrons.p4) > 1

        def evaluate_cuts(self, products):
            if products.z.p4[0].M() > 5:
                self.pass_cut('z_mass')

    def __init__(self, **kwargs):
        Analyzer.__init__(self)

        self.z = self.produces(Candidates, 'z', 'z_candidate_')

        self.uses('vertices', 'std::vector<reco::Vertex>', kwargs['vertex_collection'])
        self.uses('jets', 'std::vector<pat::Jet>', kwargs['jet_collection'])
        self.uses('muons', 'std::vector<pat::Muon>', kwargs['muon_collection'])
        self.uses('electrons', 'std::vector<pat::Electron>', kwargs['electron_collection'])
        self.uses('mets', 'std::vector<pat::MET>', kwargs['met_collection'])

        self.new_category(TestAnalyzer.TwoMuonsCategory('two_muons', 'At least 2 muons category'))
        self.new_category(TestAnalyzer.TwoElectronsCategory('two_electrons', 'At least 2 electrons category'))

    def beginJob(self):
        print("Begin job!")
        pass

    def analyze(self, event, products):
        print("Analyzing event!")

        print "The event contain:", len(event.vertices), 'vertices', len(event.jets), 'jets', len(event.muons), 'muons', len(event.electrons), 'electrons', len(event.mets), 'mets'
        if len(event.muons) >= 2:
            p4 = event.muons[0].p4() + event.muons[1].p4()
            products.z.p4.push_back(LorentzVector('ROOT::Math::PtEtaPhiE4D<float>')(p4.Pt(), p4.Eta(), p4.Phi(), p4.E()))
        elif len(products.electrons.p4) >= 2:
            p4 = products.electrons.p4[0] + products.electrons.p4[1]
            products.z.p4.push_back(LorentzVector('ROOT::Math::PtEtaPhiE4D<float>')(p4.Pt(), p4.Eta(), p4.Phi(), p4.E()))

        # Access product produced by the Jets producer
        for z in products.z.p4:
            print "Z candidate mass:", z.M()

    def endJob(self):
        print("End job!")
