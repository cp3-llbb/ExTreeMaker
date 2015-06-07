__author__ = 'obondu'

import Models.Vertices
from Producer import Producer

class Vertices(Producer):

    def __init__(self, name, vertex_collection):
        Producer.__init__(self, name)

        self.uses('vertices', 'std::vector<reco::Vertex>', vertex_collection)
        self.produces(Models.Vertices.Vertices, 'vertices', 'vertex_')

    def produce(self, event, products):
        for vertex in event.vertices:
            products.vertices.vertex_position.push_back(vertex.position())