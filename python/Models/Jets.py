__author__ = 'sbrochet'

from Candidates import Candidates

import ROOT

class Jets(Candidates):
    pu_jet_id = ROOT.vector('float')
