__author__ = 'obondu'

import Models.Electrons
from Producer import Producer
from Producers.Helper import fill_candidate

class Electrons(Producer):

    def __init__(self, name, electron_collection):
        Producer.__init__(self, name)

        self.uses('electrons', 'std::vector<pat::Electron>', electron_collection)
        self.produces(Models.Electrons.Electrons, 'electrons', 'electron_')

    def produce(self, event, products):
        for electron in event.electrons:
            fill_candidate(electron, products.electrons)
            products.electrons.electron_isLooseElectron.push_back(True) # fixme: implement ID criteria
            products.electrons.electron_isTightElectron.push_back(True)
