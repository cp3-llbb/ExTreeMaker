__author__ = 'sbrochet'

from pytree import TreeModel
from Core import Classes

class GenParticles(TreeModel):
    p4 = Classes.LorentzVectorCollection
    y = Classes.FloatCollection

    pdg_id = Classes.Int16Collection
    status = Classes.Int8Collection
    status_flags = Classes.Int16Collection

    mothers_index = Classes.UInt16CollectionCollection
