__author__ = 'obondu'

from Tools import parse_effective_areas_file

import Core.Configuration
import Models.Muons
from Producer import Producer
from Producers.Helper import fill_candidate, fill_isolations

class Muons(Producer):

    def __init__(self, name, prefix, muon_collection, vertex_collection, **kwargs):
        Producer.__init__(self, name)

        self._effective_areas_R03 = kwargs['effective_areas_R03'] if 'effective_areas_R03' in kwargs else None
        self._effective_areas_R04 = kwargs['effective_areas_R04'] if 'effective_areas_R04' in kwargs else None

        self.uses(name, 'std::vector<pat::Muon>', muon_collection)
        self.uses('vertices', 'std::vector<reco::Vertex>', vertex_collection)
        self.uses('rho', 'double', 'fixedGridRhoFastjetAll')
        self.produces(Models.Muons.Muons, name, prefix)

    def produce(self, event, products):
        muons = getattr(event, self._name)
        product = getattr(products, self._name)
        primary_vertex = event.vertices[0]
        rho = event.rho[0]
        for muon in muons:
            fill_candidate(muon, product)
            product.isLoose.push_back(muon.isLooseMuon())
            product.isMedium.push_back(muon.isMediumMuon())
            product.isSoft.push_back(muon.isSoftMuon(primary_vertex))
            product.isTight.push_back(muon.isTightMuon(primary_vertex))
            product.isHighPt.push_back(muon.isHighPtMuon(primary_vertex))

            pfIso = muon.pfIsolationR03()
            fill_isolations(muon, "R03", pfIso.sumChargedHadronPt, pfIso.sumNeutralHadronEt,
                                pfIso.sumPhotonEt, pfIso.sumPUPt, rho, muon.eta(), self._effective_areas_R03, product)

            pfIso = muon.pfIsolationR04()
            fill_isolations(muon, "R04", pfIso.sumChargedHadronPt, pfIso.sumNeutralHadronEt,
                                pfIso.sumPhotonEt, pfIso.sumPUPt, rho, muon.eta(), self._effective_areas_R04, product)


_muon_effective_areas_R03 = parse_effective_areas_file("cp3_llbb/ExTreeMaker/data/"
                                                       "effAreaMuons_cone03_pfNeuHadronsAndPhotons.txt")
_muon_effective_areas_R04 = parse_effective_areas_file("cp3_llbb/ExTreeMaker/data/"
                                                       "effAreaMuons_cone04_pfNeuHadronsAndPhotons.txt")

default_configuration = Core.Configuration.Producer(name='muons', clazz=Muons, prefix='muon_',
                                                    muon_collection='slimmedMuons',
                                                    vertex_collection='offlineSlimmedPrimaryVertices',
                                                    effective_areas_R03=_muon_effective_areas_R03,
                                                    effective_areas_R04=_muon_effective_areas_R04)
