__author__ = 'obondu'

import Models.Electrons
from Producer import Producer
from Producers.Helper import fill_candidate, fill_isolations

class Electrons(Producer):

    def __init__(self, name, prefix, electron_collection, **kwargs):
        Producer.__init__(self, name)

        self._effective_areas_R03 = kwargs['effective_areas_R03'] if 'effective_areas_R03' in kwargs else None
        self._effective_areas_R04 = kwargs['effective_areas_R04'] if 'effective_areas_R04' in kwargs else None

        self.uses(name, 'std::vector<pat::Electron>', electron_collection)
        self.uses('rho', 'double', 'fixedGridRhoFastjetAll')
        self.produces(Models.Electrons.Electrons, name, prefix)

    def produce(self, event, products):
        electrons = getattr(event, self._name)
        product = getattr(products, self._name)
        rho = event.rho[0]
        for electron in electrons:
            fill_candidate(electron, product)
            product.isLooseElectron.push_back(True) # fixme: implement ID criteria
            product.isTightElectron.push_back(True)

            eta = electron.superCluster().eta()
            pfIso = electron.pfIsolationVariables()
            fill_isolations(electron, "R03", pfIso.sumChargedHadronPt, pfIso.sumNeutralHadronEt,
                                pfIso.sumPhotonEt, pfIso.sumPUPt, rho, eta, self._effective_areas_R03, product)

            fill_isolations(electron, "R04", electron.chargedHadronIso(), electron.neutralHadronIso(),
                                electron.photonIso(), electron.puChargedHadronIso(), rho, eta,
                                self._effective_areas_R04, product)
