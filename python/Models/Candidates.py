__author__ = 'sbrochet'

from pytree import TreeModel
from ROOT import std

class Candidates(TreeModel):
    p4 = std.vector('ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiE4D<float>>')