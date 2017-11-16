"""
"""
from __future__ import print_function, absolute_import
from six import iteritems, iterkeys, itervalues
from six.moves import range

import numpy as np


class PropertyCard(object):

    table_reader = None
    dtype = None
    """:type: np.dtype"""

    def __init__(self, bdf_data):
        self.bdf_data = bdf_data

        self.data = np.zeros(0, dtype=self.dtype)
        self.index = {}

        self._current_index = -1
        self._current_data = None

    def read_h5(self, h5f):
        data = self.table_reader.read(h5f)
        if data is not None:
            self.set_data(self.table_reader.read(h5f))

    def resize(self, new_size):
        self._current_index = -1
        self._current_data = None

        self.data.resize(new_size)

    def set_data(self, data):
        self.resize(data.size)

        np.copyto(self.data, data)

        self.update()

    def update(self):
        self.index.clear()

        pid = self.data['PID']

        for i in range(self.data.size):
            self.index[pid[i]] = i

    def set_pid(self, pid):
        try:
            self._current_index = self.index[pid]
        except KeyError:
            raise ValueError('Unknown PID! %d' % pid)

        try:
            self._current_data = self.data[self._current_index]
        except IndexError:
            raise ValueError('PID %d not found in data!' % pid)