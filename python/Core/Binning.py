__author__ = 'sbrochet'

from interval import Interval

class OneDimensionBinning:
    def __init__(self):
        self._binning = []

    def add(self, lower_bound, upper_bound, value):
        interval = Interval(lower_bound, upper_bound, upper_closed=False)
        interval._value = value

        self._binning.append(interval)

    def get(self, x):
        """
        Return the value associated with the bin containing 'x'
        :param x: The parameter of interest
        :return: The value associated with the bin containing 'x', or None if there's no such bin
        """

        for interval in self._binning:
            if x in interval:
                return interval._value

        return None

    def __str__(self):
        return self._binning.__str__()