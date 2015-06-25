__author__ = 'obondu'

import Core.Configuration
import Models.Vertices
from Producer import Producer


class Vertices(Producer):
    def __init__(self, name, prefix, vertex_collection, **kwargs):
        Producer.__init__(self, name, **kwargs)

        self.uses(name, 'std::vector<reco::Vertex>', vertex_collection)
        self.produces(Models.Vertices.Vertices, name, prefix)

    def produce(self, event, products):
        vertices = getattr(event, self._name)
        product = getattr(products, self._name)
        for vertex in vertices:
            if not self.pass_cut(vertex):
                continue

            product.position.push_back(vertex.position())


default_configuration = Core.Configuration.Producer(name='vertices', prefix='vertex_', clazz=Vertices,
                                                    vertex_collection='offlineSlimmedPrimaryVertices')
