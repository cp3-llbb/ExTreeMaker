__author__ = 'obondu'

from Leptons import Leptons

import ROOT

class Electrons(Leptons):
    isLooseElectron = ROOT.vector('bool')
    isTightElectron = ROOT.vector('bool')