__author__ = 'obondu'

import Models.Electrons
from Producer import Producer
from Producers.Helper import fill_candidate, fill_isolations

class Electrons(Producer):

    def __init__(self, name, prefix, electron_collection):
        Producer.__init__(self, name)

        self.uses(name, 'std::vector<pat::Electron>', electron_collection)
        self.produces(Models.Electrons.Electrons, name, prefix)

    def produce(self, event, products):
        electrons = getattr(event, self._name)
        product = getattr(products, self._name)
        for electron in electrons:
            fill_candidate(electron, product)
            product.isLooseElectron.push_back(True) # fixme: implement ID criteria
            product.isTightElectron.push_back(True)

            pfIso = electron.pfIsolationVariables()
            fill_isolations(electron, "R03", pfIso.sumChargedHadronPt, pfIso.sumNeutralHadronEt,
                                pfIso.sumPhotonEt, pfIso.sumPUPt, product)

            fill_isolations(electron, "R04", electron.chargedHadronIso(), electron.neutralHadronIso(),
                                electron.photonIso(), electron.puChargedHadronIso(), product)
