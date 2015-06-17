__author__ = 'obondu'

from Leptons import Leptons

from Core import Classes

class Electrons(Leptons):
    supercluster_eta = Classes.FloatCollection
    supercluster_phi = Classes.FloatCollection

    isLooseElectron = Classes.BoolCollection
    isTightElectron = Classes.BoolCollection