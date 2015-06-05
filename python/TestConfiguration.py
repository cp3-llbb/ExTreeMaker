__author__ = 'sbrochet'

from Core.Configuration import Configuration, Bunch, Collection

from TestAnalyzer import TestAnalyzer
from Producers.Vertices import Vertices
from Producers.Jets import Jets
from Producers.Muons import Muons

class TestConfiguration(Configuration):

    analyzer = TestAnalyzer

    producers = [
        Bunch(alias='vertices', clazz=Vertices, vertex_collection='offlineSlimmedPrimaryVertices'),
        Bunch(alias='jets', clazz=Jets, jet_collection='slimmedJets'),
        Bunch(alias='muons', clazz=Muons, muon_collection='slimmedMuons', vertex_collection='offlineSlimmedPrimaryVertices')
    ]

    collections = [
        Collection(alias='vertices', type='std::vector<reco::Vertex>', input_tag='offlineSlimmedPrimaryVertices'),
        Collection(alias='jets', type='std::vector<pat::Jet>', input_tag='slimmedJets'),
        Collection(alias='muons', type='std::vector<pat::Muon>', input_tag='slimmedMuons')
    ]

    analyzer_configuration = {
        'vertex_collection': 'offlineSlimmedPrimaryVertices',
        'jet_collection': 'slimmedJets',
        'muon_collection': 'slimmedMuons'
    }