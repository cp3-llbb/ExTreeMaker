__author__ = 'sbrochet'

import Models.Jets
from Producer import Producer

import Core.Configuration
from Core import Classes

from Helper import fill_candidate

class Jets(Producer):

    def __init__(self, name, prefix, jet_collection, **kwargs):
        Producer.__init__(self, name, **kwargs)

        self.btag_branch_created = False

        self.uses(name, 'std::vector<pat::Jet>', jet_collection)
        self.produces(Models.Jets.Jets, name, prefix)

    def produce(self, event, products):
        jets = getattr(event, self._name)
        product = getattr(products, self._name)
        for jet in jets:
            if not self.pass_cut(jet):
                continue

            fill_candidate(jet, product)

            product.jecFactor.push_back(jet.jecFactor(0))
            product.area.push_back(jet.jetArea())
            product.partonFlavor.push_back(jet.partonFlavour())
            product.hadronFlavor.push_back(jet.hadronFlavour())

            if jet.hasUserFloat('pileupJetId:fullDiscriminant'):
                product.pu_jet_id.push_back(jet.userFloat('pileupJetId:fullDiscriminant'))

            product.vtxMass.push_back(jet.userFloat('vtxMass'))

            btag_discris = jet.getPairDiscri()
            for btag_discri in btag_discris:
                if not products.frozen() and not self.btag_branch_created:
                    products.new_product_branch(product, btag_discri.first, Classes.FloatCollection)

                getattr(product, btag_discri.first).push_back(btag_discri.second)

            if not products.frozen() and not self.btag_branch_created:
               self.btag_branch_created = True

default_configuration = Core.Configuration.Producer(name='jets', clazz=Jets, prefix='jet_',
                                                    jet_collection='slimmedJets')
