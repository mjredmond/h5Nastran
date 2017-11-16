"""
"""
from __future__ import print_function, absolute_import
from six import iteritems, itervalues
from six.moves import range

import numpy as np


class TableIndex(object):

    def __init__(self, initial_size=16384, cols=1):

        if cols == 2:
            initial_size = (initial_size, cols)
            self._columns = 2
        else:
            self._columns = 1

        self._data = np.empty(initial_size, dtype=np.int64)
        self._used = 0

    def append(self, data):
        if self._used == self._data.shape[0]:
            if self._columns == 1:
                self._data.resize(2 * self._data.size)
            else:
                rows = self._data.shape[0] * 2
                self._data.resize((rows, self._columns))

        self._data[self._used] = data
        self._used += 1

    def squeeze(self):
        if self._columns == 1:
            self._data.resize(self._used)
        else:
            self._data.resize((self._used, self._columns))

    @property
    def used(self):
        return self._used

    @property
    def data(self):
        return self._data
