__author__ = 'sbrochet'

from ROOT.Math import LorentzVector

def fill_candidate(candidate, product):
    """
    Fill values from candidate into the product
    :param candidate: a candidate
    :param Models.Candidates.Candidates product: the product to fill
    :return:
    """
    p4 = LorentzVector('ROOT::Math::PtEtaPhiE4D<float>')(candidate.pt(), candidate.eta(), candidate.phi(), candidate.energy())
    product.p4.push_back(p4)
    product.y.push_back(candidate.rapidity())
    product.charge.push_back(candidate.charge())

    gen = candidate.genParticle()
    if gen:
        product.has_matched_gen_particle.push_back(True)
        p4 = LorentzVector('ROOT::Math::PtEtaPhiE4D<float>')(gen.pt(), gen.eta(), gen.phi(), gen.energy())
        product.gen_p4.push_back(p4)
        product.gen_y.push_back(gen.rapidity())
        product.gen_charge.push_back(gen.charge())
    else:
        product.has_matched_gen_particle.push_back(False)
        product.gen_p4.push_back(LorentzVector('ROOT::Math::PtEtaPhiE4D<float>')())
        product.gen_y.push_back(0)
        product.gen_charge.push_back(0)
