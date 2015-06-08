__author__ = 'sbrochet'

from pytree import TreeModel
from ROOT import std
from ROOT.Math import LorentzVector

class Candidates(TreeModel):
    p4 = std.vector('ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiE4D<float>>')
    y = std.vector('float')
    charge = std.vector('int8_t')

    has_matched_gen_particle = std.vector('bool')
    gen_p4 = std.vector('ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiE4D<float>>')
    gen_y = std.vector('float')
    gen_charge = std.vector('int8_t')