__author__ = 'obondu'

from Candidates import Candidates

import ROOT

class Vertices(Candidates):
    position = ROOT.vector('ROOT::Math::XYZPoint')