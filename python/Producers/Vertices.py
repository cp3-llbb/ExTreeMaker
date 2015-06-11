__author__ = 'obondu'

import Models.Vertices
from Producer import Producer

class Vertices(Producer):

    def __init__(self, name, prefix, vertex_collection):
        Producer.__init__(self, name)

        self.uses(name, 'std::vector<reco::Vertex>', vertex_collection)
        self.produces(Models.Vertices.Vertices, name, prefix)

    def produce(self, event, products):
        vertices = getattr(event, self._name)
        product = getattr(products, self._name)
        for vertex in vertices:
            product.position.push_back(vertex.position())