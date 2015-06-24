__author__ = 'sbrochet'

from Producers.Producer import Producer
import Core.Configuration
import Models.HLT

class HLT(Producer):

    def __init__(self, name, prefix, **kwargs):
        Producer.__init__(self, name)

        self.uses('triggerResults', 'edm::TriggerResults', ('TriggerResults', '', 'HLT'))
        self.uses('prescales', 'pat::PackedTriggerPrescales', 'patTrigger')

        self.produces(Models.HLT.HLT, name, prefix)

    def produce(self, event, products):
        product = getattr(products, self._name)

        trigger_names = event.trigger_names(event.triggerResults)

        for i in xrange(0, event.triggerResults.size()):
            if event.triggerResults.accept(i):
                trigger_name = trigger_names.triggerName(i)
                if trigger_name == 'HLTriggerFinalPath':
                    continue  # This one is pretty useless...
                if trigger_name[0] == 'A':
                    continue  # Remove AlCa HLT paths

                product.paths.push_back(trigger_name)

                if event.prescales:
                    product.prescales.push_back(event.prescales.getPrescaleForIndex(i))

default_configuration = Core.Configuration.Producer(name='hlt', prefix='hlt_', clazz=HLT)
