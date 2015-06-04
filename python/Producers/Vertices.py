__author__ = 'obondu'

import Models.Vertices
from Producer import Producer
# from ROOT.Math import XYZPointF

class Vertices(Producer):

    def __init__(self, name, vertex_collection):
        Producer.__init__(self, name)

        self.uses('vertices', 'std::vector<reco::Vertex>', vertex_collection)
        self.produces(Models.Vertices.Vertices, 'vertices', 'vertex_')

    def produce(self, event, products):
        for vertex in event.vertices:
            # p3 = XYZPointF('ROOT::Math::PositionVector3D<ROOT::Math::Cartesian3D<float>>')(0., 0., 0.)
            # products.vertices.vertex_p3.push_back(p3)
            products.vertices.vertex_sumpt2.push_back(0.5) #fixme: stupid for now
