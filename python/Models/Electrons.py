__author__ = 'obondu'

from Candidates import Candidates

import ROOT

class Electrons(Candidates):
    isLooseElectron = ROOT.vector('bool')
    isTightElectron = ROOT.vector('bool')