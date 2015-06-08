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
        product = products.muons
        primary_vertex = event.vertices[0]
        for muon in event.muons:
            fill_candidate(muon, product)
            product.isLoose.push_back(muon.isLooseMuon())
            product.isMedium.push_back(muon.isMediumMuon())
            product.isSoft.push_back(muon.isSoftMuon(primary_vertex))
            product.isTight.push_back(muon.isTightMuon(primary_vertex))
            product.isHighPt.push_back(muon.isHighPtMuon(primary_vertex))
