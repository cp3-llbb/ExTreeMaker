__author__ = 'sbrochet'

from Core.Configuration import Configuration, Bunch, Collection

from TestAnalyzer import TestAnalyzer
from Producers.Vertices import Vertices
from Producers.Jets import Jets
from Producers.Muons import Muons
from Producers.Electrons import Electrons
from Producers.METs import METs

class TestConfiguration(Configuration):

    analyzer = TestAnalyzer

    producers = [
        Bunch(alias='vertices', clazz=Vertices, vertex_collection='offlineSlimmedPrimaryVertices'),
        Bunch(alias='jets', clazz=Jets, prefix='jet_', jet_collection='slimmedJets',
              btag_collections=['pfCombinedInclusiveSecondaryVertexV2BJetTags']),
        Bunch(alias='puppiJets', clazz=Jets, prefix='puppijet_', jet_collection='slimmedJetsPuppi'),
        Bunch(alias='muons', clazz=Muons, muon_collection='slimmedMuons', vertex_collection='offlineSlimmedPrimaryVertices'),
        Bunch(alias='electrons', clazz=Electrons, electron_collection='slimmedElectrons'),
        Bunch(alias='mets', clazz=METs, met_collection='slimmedMETs')
    ]

    collections = [
        Collection(alias='vertices', type='std::vector<reco::Vertex>', input_tag='offlineSlimmedPrimaryVertices'),
        Collection(alias='jets', type='std::vector<pat::Jet>', input_tag='slimmedJets'),
        Collection(alias='muons', type='std::vector<pat::Muon>', input_tag='slimmedMuons'),
        Collection(alias='electrons', type='std::vector<pat::Electron>', input_tag='slimmedElectrons'),
        Collection(alias='mets', type='std::vector<pat::MET>', input_tag='slimmedMETs')
    ]

    analyzer_configuration = {
        'vertex_collection': 'offlineSlimmedPrimaryVertices',
        'jet_collection': 'slimmedJets',
        'muon_collection': 'slimmedMuons',
        'electron_collection': 'slimmedElectrons',
        'met_collection': 'slimmedMETs'
    }
