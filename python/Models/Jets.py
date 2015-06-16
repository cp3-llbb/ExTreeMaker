__author__ = 'sbrochet'

from Candidates import Candidates
from Core import Classes

class Jets(Candidates):
    area = Classes.FloatCollection
    partonFlavor = Classes.Int8Collection
    hadronFlavor = Classes.Int8Collection
    jecFactor = Classes.FloatCollection

    pu_jet_id = Classes.FloatCollection
    vtxMass = Classes.FloatCollection

    btag = Classes.StringFloatMapCollection
