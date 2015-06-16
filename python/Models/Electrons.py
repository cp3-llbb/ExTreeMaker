__author__ = 'obondu'

from Leptons import Leptons

from Core import Classes

class Electrons(Leptons):
    isLooseElectron = Classes.BoolCollection
    isTightElectron = Classes.BoolCollection