__author__ = 'obondu'

from Candidates import Candidates

import ROOT

class Muons(Candidates):
    isLooseMuon = ROOT.vector('bool')
    isTightMuon = ROOT.vector('bool')