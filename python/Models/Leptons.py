__author__ = 'sbrochet'

from Models.Candidates import Candidates
from ROOT import vector

class Leptons(Candidates):
    chargedHadronIsoR03 = vector('float')
    chargedHadronIsoR04 = vector('float')
    neutralHadronIsoR03 = vector('float')
    neutralHadronIsoR04 = vector('float')
    photonIsoR03 = vector('float')
    photonIsoR04 = vector('float')
    relativeIsoR03 = vector('float')
    relativeIsoR04 = vector('float')
    relativeIsoR03_deltaBeta = vector('float')
    relativeIsoR04_deltaBeta = vector('float')
    relativeIsoR03_withEA = vector('float')
    relativeIsoR04_withEA = vector('float')
