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

def fill_isolations(candidate, cone_size, chargedHadronIso, neutralHadronIso, photonIso, puIso, product):
    """

    :param candidate:
    :param cone_size: The cone size. Can be "R04" or "R03"
    :param chargedHadronIso:
    :param neutralHadronIso:
    :param photonIso:
    :param puIso:
    :param product:
    :return:
    """

    def get_product(name):
        return getattr(product, "%s%s" % (name, cone_size)) if "%s" not in name else getattr(product, name % cone_size)

    get_product("chargedHadronIso").push_back(chargedHadronIso)
    get_product("neutralHadronIso").push_back(neutralHadronIso)
    get_product("photonIso").push_back(photonIso)

    get_product("relativeIso").push_back((chargedHadronIso + neutralHadronIso + photonIso) / candidate.pt())
    get_product("relativeIso%s_deltaBeta").push_back((chargedHadronIso + max((neutralHadronIso + photonIso) - 0.5 * puIso,
                                                                        0.0)) / candidate.pt())
    get_product("relativeIso%s_withEA").push_back(0)  # FIXME: Needs EA values
