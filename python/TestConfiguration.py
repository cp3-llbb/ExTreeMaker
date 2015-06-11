__author__ = 'sbrochet'

from Core.Configuration import Configuration, Bunch, Collection
from Tools import parse_effective_areas_file

from TestAnalyzer import TestAnalyzer
from Producers.Event import Event
from Producers.Vertices import Vertices
from Producers.Jets import Jets
from Producers.Muons import Muons
from Producers.Electrons import Electrons
from Producers.METs import METs


class TestConfiguration(Configuration):

    analyzer = TestAnalyzer

    electron_effective_areas = parse_effective_areas_file("RecoEgamma/ElectronIdentification/data/PHYS14/"
                                                          "effAreaElectrons_cone03_pfNeuHadronsAndPhotons.txt")

    muon_effective_areas_R03 = parse_effective_areas_file("cp3_llbb/ExTreeMaker/data/"
                                                          "effAreaMuons_cone03_pfNeuHadronsAndPhotons.txt")
    muon_effective_areas_R04 = parse_effective_areas_file("cp3_llbb/ExTreeMaker/data/"
                                                          "effAreaMuons_cone04_pfNeuHadronsAndPhotons.txt")

    producers = [
        Bunch(alias='event', prefix='event_', clazz=Event),
        Bunch(alias='vertices', clazz=Vertices, vertex_collection='offlineSlimmedPrimaryVertices'),
        Bunch(alias='jets', clazz=Jets, prefix='jet_', jet_collection='slimmedJets',
              btag_collections=['pfCombinedInclusiveSecondaryVertexV2BJetTags']),
        Bunch(alias='puppiJets', clazz=Jets, prefix='puppijet_', jet_collection='slimmedJetsPuppi'),
        Bunch(alias='muons', clazz=Muons, prefix='muon_', muon_collection='slimmedMuons',
              vertex_collection='offlineSlimmedPrimaryVertices', effective_areas_R03=muon_effective_areas_R03,
              effective_areas_R04=muon_effective_areas_R04),
        Bunch(alias='electrons', clazz=Electrons, prefix='electron_', electron_collection='slimmedElectrons',
              effective_areas_R03=electron_effective_areas),
        Bunch(alias='mets', clazz=METs, prefix='met_', met_collection='slimmedMETs')
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