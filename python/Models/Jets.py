__author__ = 'sbrochet'

from Candidates import Candidates

import ROOT

class Jets(Candidates):
    area = ROOT.vector('float')
    partonFlavor = ROOT.vector('int8_t')
    hadronFlavor = ROOT.vector('int8_t')
    jecFactor = ROOT.vector('float')

    pu_jet_id = ROOT.vector('float')
    vtxMass = ROOT.vector('float')

    btag = ROOT.vector('std::map<std::string, float>')
