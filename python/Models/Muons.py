__author__ = 'obondu'

from Candidates import Candidates

import ROOT

class Muons(Candidates):
    isLoose = ROOT.vector('bool')
    isMedium = ROOT.vector('bool')
    isSoft = ROOT.vector('bool')
    isTight = ROOT.vector('bool')
    isHighPt = ROOT.vector('bool')