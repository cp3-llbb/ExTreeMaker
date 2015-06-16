__author__ = 'obondu'

from Leptons import Leptons

from Core import Classes

class Muons(Leptons):
    isLoose = Classes.BoolCollection
    isMedium = Classes.BoolCollection
    isSoft = Classes.BoolCollection
    isTight = Classes.BoolCollection
    isHighPt = Classes.BoolCollection