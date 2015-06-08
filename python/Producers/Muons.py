__author__ = 'obondu'

import Models.Muons
from Producer import Producer
from Producers.Helper import fill_candidate

class Muons(Producer):

    def __init__(self, name, muon_collection, vertex_collection):
        Producer.__init__(self, name)

        self.uses('muons', 'std::vector<pat::Muon>', muon_collection)
        self.uses('vertices', 'std::vector<reco::Vertex>', vertex_collection)
        self.produces(Models.Muons.Muons, 'muons', 'muon_')

    def produce(self, event, products):
        for muon in event.muons:
            fill_candidate(muon, products.muons)
            products.muons.muon_isLooseMuon.push_back(muon.isLooseMuon())
            products.muons.muon_isTightMuon.push_back(muon.isTightMuon(event.vertices[0]))
