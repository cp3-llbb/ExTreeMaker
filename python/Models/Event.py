__author__ = 'sbrochet'

from pytree import TreeModel
from pytree import FloatCol, ULongCol, IntCol

from ROOT import std

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
    pdf_id = std.pair('int, int')
    pdf_x = std.pair('float, float')

    n_ME_partons = IntCol()
    n_ME_partons_filtered = IntCol()
