__author__ = 'obondu'

from pytree import TreeModel
import ROOT

class Vertices(TreeModel):
    position = ROOT.vector('ROOT::Math::XYZPoint')
