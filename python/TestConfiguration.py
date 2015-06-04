__author__ = 'sbrochet'

from Core.Configuration import Configuration, Bunch, Collection

from TestAnalyzer import TestAnalyzer
from Producers.Jets import Jets

class TestConfiguration(Configuration):

    analyzer = TestAnalyzer

    producers = [
        Bunch(alias='jets', clazz=Jets, jet_collection='slimmedJets')
    ]

    collections = [
        Collection(alias='jets', type='std::vector<pat::Jet>', input_tag='slimmedJets')
    ]

    analyzer_configuration = {
        'jet_collection': 'slimmedJets'
    }