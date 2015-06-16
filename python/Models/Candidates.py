__author__ = 'sbrochet'

from pytree import TreeModel
from Core import Classes

class Candidates(TreeModel):
    p4 = Classes.LorentzVectorCollection
    y = Classes.FloatCollection
    charge = Classes.Int8Collection

    has_matched_gen_particle = Classes.BoolCollection
    gen_p4 = Classes.LorentzVectorCollection
    gen_y = Classes.FloatCollection
    gen_charge = Classes.Int8Collection