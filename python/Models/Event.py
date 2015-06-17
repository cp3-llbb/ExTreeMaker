__author__ = 'sbrochet'

from pytree import TreeModel
from pytree import FloatCol, ULongCol, IntCol

from Core import Classes

class Event(TreeModel):
    run = ULongCol()
    lumi = ULongCol()
    event = ULongCol()

    rho = FloatCol()

    npu = IntCol()
    true_interactions = FloatCol()

    pt_hat = FloatCol()
    weight = FloatCol(default=1)

    alpha_QCD = FloatCol()
    alpha_QED = FloatCol()
    q_scale = FloatCol()
    pdf_id = Classes.IntIntPair
    pdf_x = Classes.FloatFloatPair

    n_ME_partons = IntCol()
    n_ME_partons_filtered = IntCol()

    lhe_originalXWGTUP = FloatCol()
    lhe_SCALUP = FloatCol()
    lhe_weights = Classes.StringFloatPairCollection
