__author__ = 'sbrochet'

import ROOT

"""
Defines some often used template classes across the framework. Template class creation is a rather heavy operation
 using pyROOT.
"""

LorentzVector = ROOT.Math.LorentzVector('ROOT::Math::PtEtaPhiE4D<float>')
LorentzVectorCollection = ROOT.std.vector('ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiE4D<float>>')

StringFloatMap = ROOT.std.map('std::string, float')
StringFloatMapCollection = ROOT.std.vector('std::map<std::string, float>')

IntIntPair = ROOT.std.pair('int, int')
StringFloatPair = ROOT.std.pair('std::string, float')
FloatFloatPair = ROOT.std.pair('float, float')

StringFloatPairCollection = ROOT.std.vector('std::pair<std::string, float>')

StringCollection = ROOT.std.vector('std::string')
FloatCollection = ROOT.std.vector('float')
BoolCollection = ROOT.std.vector('bool')
Int8Collection = ROOT.std.vector('int8_t')
Int16Collection = ROOT.std.vector('int16_t')
UInt16Collection = ROOT.std.vector('uint16_t')

UInt16CollectionCollection = ROOT.std.vector('std::vector<uint16_t>')
