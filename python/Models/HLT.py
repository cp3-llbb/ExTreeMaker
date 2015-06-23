__author__ = 'sbrochet'

from Core.Classes import StringCollection, UInt16Collection

from pytree import TreeModel

class HLT(TreeModel):
    paths = StringCollection
    prescales = UInt16Collection
