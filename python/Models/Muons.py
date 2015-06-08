__author__ = 'obondu'

from Leptons import Leptons

import ROOT

class Muons(Leptons):
    isLoose = ROOT.vector('bool')
    isMedium = ROOT.vector('bool')
    isSoft = ROOT.vector('bool')
    isTight = ROOT.vector('bool')
    isHighPt = ROOT.vector('bool')