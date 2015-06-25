__author__ = 'obondu'

import Core.Configuration
import Models.METs
from Producer import Producer
from Producers.Helper import fill_candidate


class METs(Producer):
    def __init__(self, name, prefix, met_collection, **kwargs):
        Producer.__init__(self, name, **kwargs)

        self.uses(name, 'std::vector<pat::MET>', met_collection)
        self.produces(Models.METs.METs, name, prefix)

    def produce(self, event, products):
        mets = getattr(event, self._name)
        product = getattr(products, self._name)
        for met in mets:
            if not self.pass_cut(met):
                continue
            fill_candidate(met, product)


default_configuration = Core.Configuration.Producer(name='mets', clazz=METs, prefix='met_',
                                                    met_collection='slimmedMETs')
