__author__ = 'obondu'

from Tools import parse_effective_areas_file

import Core.Configuration
import Models.Electrons
from Producer import Producer
from Producers.Helper import fill_candidate, fill_isolations

class Electrons(Producer):

    def __init__(self, name, prefix, electron_collection, **kwargs):
        Producer.__init__(self, name, **kwargs)

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
            if not self.pass_cut(electron):
                continue

            fill_candidate(electron, product)

            product.supercluster_eta.push_back(electron.superCluster().eta())
            product.supercluster_phi.push_back(electron.superCluster().phi())

            product.isLooseElectron.push_back(True) # fixme: implement ID criteria
            product.isTightElectron.push_back(True)

            eta = electron.superCluster().eta()
            pfIso = electron.pfIsolationVariables()
            fill_isolations(electron, "R03", pfIso.sumChargedHadronPt, pfIso.sumNeutralHadronEt,
                                pfIso.sumPhotonEt, pfIso.sumPUPt, rho, eta, self._effective_areas_R03, product)

            fill_isolations(electron, "R04", electron.chargedHadronIso(), electron.neutralHadronIso(),
                                electron.photonIso(), electron.puChargedHadronIso(), rho, eta,
                                self._effective_areas_R04, product)


_electron_effective_areas = parse_effective_areas_file("RecoEgamma/ElectronIdentification/data/PHYS14/"
                                                       "effAreaElectrons_cone03_pfNeuHadronsAndPhotons.txt")

default_configuration = Core.Configuration.Producer(name='electrons', clazz=Electrons, prefix='electron_',
                                                    electron_collection='slimmedElectrons',
                                                    effective_areas_R03=_electron_effective_areas)
