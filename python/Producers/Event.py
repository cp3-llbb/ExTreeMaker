__author__ = 'sbrochet'

from DataFormats.FWLite import Handle
from Producers.Producer import Producer
from Tools import loop

import Core.Configuration
import Core.Classes
import Models.Event

class Event(Producer):
    # noinspection PyUnusedLocal
    def __init__(self, name, prefix, **kwargs):
        Producer.__init__(self, name)

        self.uses('puInfo', 'std::vector<PileupSummaryInfo>', 'addPileupInfo')
        self.uses('genInfo', 'GenEventInfoProduct', 'generator')
        self.uses('lheInfo', 'LHEEventProduct', 'externalLHEProducer')
        self.uses('rho', 'double', 'fixedGridRhoFastjetAll')

        self.produces(Models.Event.Event, name, prefix)

    def produce(self, event, products):

        product = getattr(products, self._name)

        if not products.frozen():

            # Retrieve mapping between weights ids and name
            # This is stored as a plain XML text inside the LHERunInfoProduct
            run = event.run_object()
            lhe_run_info_handle = Handle('LHERunInfoProduct')
            if run.getByLabel('externalLHEProducer', lhe_run_info_handle):
                lhe_run_info = lhe_run_info_handle.product()

                xml = ''
                for header in loop(lhe_run_info.headers_begin(), lhe_run_info.headers_end()):
                    if header.tag().strip() != 'initrwgt':
                        continue
                    xml = '\n'.join([x.strip() for x in header.lines()])
                    break

                products.add_metadata('lhe_weights', xml)

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

        # LHE weights
        if event.lheInfo:
            product.lhe_originalXWGTUP = event.lheInfo.originalXWGTUP()
            product.lhe_SCALUP = event.lheInfo.hepeup().SCALUP
            for weight in event.lheInfo.weights():
                product.lhe_weights.push_back(Core.Classes.StringFloatPair(weight.id, weight.wgt))

default_configuration = Core.Configuration.Producer(name='event', prefix='event_', clazz=Event)
