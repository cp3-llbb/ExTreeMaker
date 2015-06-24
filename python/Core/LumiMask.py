__author__ = 'sbrochet'

import FWCore.ParameterSet.Types as cms

class LumiMask:

    def __init__(self, lumi_mask):

        # lumi_mask is a cms.VLuminosityBlockRange
        # Convert it to an array of cms.LuminosityBlockRange
        self.lumi_mask = []
        for l in lumi_mask:
            self.lumi_mask.append(cms.LuminosityBlockRange(l))

    def __contains__(self, item):
        """
        Test if the given run and luminosity section are in the mask.
        :param item: A tuple of format (run, lumi)
        :return: True if the couple run / lumi are in the mask, False otherwise
        """

        assert len(item) == 2

        run = item[0]
        lumi = item[1]

        for l in self.lumi_mask:
            if l.start() == run and l.startSub() <= lumi <= l.endSub():
                return True

        return False

if __name__ == "__main__":
    # Test module

    # Craft a lumi list
    import FWCore.PythonUtilities.LumiList as LumiList

    ll = LumiList.LumiList(compactList={"132440": [[157, 378]], "132596": [[382, 382], [447, 447]],
                                        "132598": [[174, 176]], "132599": [[1, 379], [381, 437]], "132601": [[1, 207]],
                                        '1001': [[1, 2]], '1003': [[1, 1], [1, 3]]})

    mask = LumiMask(ll.getVLuminosityBlockRange())

    assert (132440, 157) in mask
    assert (132440, 300) in mask
    assert (132440, 378) in mask
    assert (132440, 379) not in mask

    assert (132599, 380) not in mask
    assert (132599, 500) not in mask

    assert (132598, 500) not in mask
    assert (132598, 0) not in mask
    assert (132598, 150) not in mask

    assert (1001, 1) in mask
    assert (1001, 2) in mask
    assert (1002, 2) not in mask
    assert (1003, 1) in mask
    assert (1003, 2) in mask
    assert (1003, 3) in mask