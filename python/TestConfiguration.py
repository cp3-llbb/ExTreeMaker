__author__ = 'sbrochet'

from Core.Configuration import Configuration, Collection

from TestAnalyzer import TestAnalyzer

import Producers.HLT
import Producers.Event
import Producers.Vertices
import Producers.Jets
import Producers.Muons
import Producers.Electrons
import Producers.METs


class TestConfiguration(Configuration):

    analyzer = TestAnalyzer

    producers = [
        Producers.HLT.default_configuration,
        Producers.Event.default_configuration,
        Producers.Vertices.default_configuration,
        Producers.Jets.default_configuration,
        Producers.Jets.default_configuration.clone(
            name='puppiJets',
            prefix='puppijet_',
            jet_collection='slimmedJetsPuppi'
        ),
        Producers.Muons.default_configuration,
        Producers.Electrons.default_configuration,
        Producers.METs.default_configuration
    ]

    collections = [
        Collection(name='vertices', type='std::vector<reco::Vertex>', input_tag='offlineSlimmedPrimaryVertices'),
        Collection(name='jets', type='std::vector<pat::Jet>', input_tag='slimmedJets'),
        Collection(name='muons', type='std::vector<pat::Muon>', input_tag='slimmedMuons'),
        Collection(name='electrons', type='std::vector<pat::Electron>', input_tag='slimmedElectrons'),
        Collection(name='mets', type='std::vector<pat::MET>', input_tag='slimmedMETs')
    ]

    analyzer_configuration = {
        'vertex_collection': 'offlineSlimmedPrimaryVertices',
        'jet_collection': 'slimmedJets',
        'muon_collection': 'slimmedMuons',
        'electron_collection': 'slimmedElectrons',
        'met_collection': 'slimmedMETs'
    }