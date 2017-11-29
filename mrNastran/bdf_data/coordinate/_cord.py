from __future__ import print_function, absolute_import
from six import iteritems, iterkeys, itervalues
from six.moves import range

import numpy as np

from .._abstract_card import AbstractCard

norm = np.linalg.norm


class CordCard(AbstractCard):

    table_reader = None
    dtype = None
    """:type: np.dtype"""

    _dtype = np.dtype([
        ('V1', np.float64, (3,)),
        ('V2', np.float64, (3,)),
        ('V3', np.float64, (3,))
    ])

    def __init__(self, bdf_data):
        super(CordCard, self).__init__(bdf_data)
        self._data = np.zeros(0, dtype=self._dtype)

    def read_h5(self, h5f):
        data = self.table_reader.read(h5f)
        if data is not None:
            self.set_data(self.table_reader.read(h5f))

    def resize(self, new_size):
        self.data.resize(new_size)
        self._data.resize(new_size)

    def set_data(self, data):
        if data is None:
            return

        self.resize(data.size)

        np.copyto(self.data, data)

