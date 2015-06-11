__author__ = 'sbrochet'

from Producers.Producer import Producer

import Core.Configuration
import Models.Event

class Event(Producer):
    # noinspection PyUnusedLocal
    def __init__(self, name, prefix, **kwargs):
        Producer.__init__(self, name)

        self.uses('puInfo', 'std::vector<PileupSummaryInfo>', 'addPileupInfo')
        self.uses('genInfo', 'GenEventInfoProduct', 'generator')
        self.uses('rho', 'double', 'fixedGridRhoFastjetAll')

        self.produces(Models.Event.Event, name, prefix)

    def produce(self, event, products):

        product = getattr(products, self._name)

        product.run = event.run()
        product.lumi = event.lumi()
        product.event = event.event()

        product.rho = event.rho[0]

        # Generator information
        if event.genInfo:
            if event.genInfo.hasBinningValues():
                product.pt_hat = event.genInfo.binningValues()[0]

            product.weight = event.genInfo.weight()

            product.n_ME_partons = event.genInfo.nMEPartons()
            product.n_ME_partons_filtered = event.genInfo.nMEPartonsFiltered()

            product.alpha_QCD = event.genInfo.alphaQCD()
            product.alpha_QED = event.genInfo.alphaQED()
            product.q_scale = event.genInfo.qScale()

            if event.genInfo.hasPDF():
                product.pdf_id = event.genInfo.pdf().id
                product.pdf_x.first = event.genInfo.pdf().x.first
                product.pdf_x.second = event.genInfo.pdf().x.second

        if event.puInfo:
            for puInfo in event.puInfo:
                if puInfo.getBunchCrossing() != 0:
                    continue

                product.npu = puInfo.getPU_NumInteractions()
                product.true_interactions = puInfo.getTrueNumInteractions()

default_configuration = Core.Configuration.Producer(name='event', prefix='event_', clazz=Event)
