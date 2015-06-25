__author__ = 'sbrochet'

from Producers.Producer import Producer
import Core.Configuration
import Models.GenParticles
from Core import Classes

import ROOT

def print_particle(p, indent_level=0):
    indent = '  ' * indent_level
    print('%sPDG id: %6d    pt: %9.2f    eta: %9.2f    phi: %9.2f    status: %3d    # mothers: %1d' %
          (indent, p.pdgId(), p.pt(), p.eta(), p.phi(), p.status(), p.numberOfMothers()))

def fill_particle(product, p):
    p4 = Classes.LorentzVector(p.pt(), p.eta(), p.phi(), p.energy())
    product.p4.push_back(p4)
    product.y.push_back(p.rapidity())

    product.pdg_id.push_back(p.pdgId())
    product.status.push_back(p.status())
    product.status_flags.push_back(p.statusFlags().flags_.to_ulong())

    mothers_index = Classes.UInt16Collection(p.numberOfMothers())
    if isinstance(p, ROOT.pat.PackedGenParticle):
        if p.numberOfMothers() > 0:
            mothers_index.push_back(p.motherRef().key())
    else:
        for m in xrange(p.numberOfMothers()):
            mothers_index.push_back(p.motherRef(m).key())
    product.mothers_index.push_back(mothers_index)

class GenParticles(Producer):

    def __init__(self, name, prefix, **kwargs):
        Producer.__init__(self, name)

        # Only status = 1 particles (stable particles)
        self.uses('packed', 'std::vector<pat::PackedGenParticle>', 'packedGenParticles')
        # Part of the event history (all status)
        self.uses('pruned', 'std::vector<reco::GenParticle>', 'prunedGenParticles')

        self.produces(Models.GenParticles.GenParticles, name + '_packed', prefix + 'packed_')
        self.produces(Models.GenParticles.GenParticles, name + '_pruned', prefix + 'pruned_')

    def produce(self, event, products):

        product_packed = getattr(products, self._name + '_packed')
        product_pruned = getattr(products, self._name + '_pruned')

        pruned = event.pruned
        for i in xrange(len(pruned)):
            fill_particle(product_pruned, pruned.at(i))

        packed = event.packed
        for i in xrange(len(packed)):
            fill_particle(product_packed, packed.at(i))

default_configuration = Core.Configuration.Producer(name='gen_particle', prefix='gen_particle_', clazz=GenParticles)
