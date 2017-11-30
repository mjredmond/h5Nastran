from __future__ import print_function, absolute_import
from six import iteritems, iterkeys, itervalues
from six.moves import range

import numpy as np

from .._abstract_card import AbstractCard


class ConstraintCard(AbstractCard):
    table_reader = None
    dtype = None
    """:type: np.dtype"""

    def __init__(self, bdf_data):
        super(ConstraintCard, self).__init__(bdf_data)

    def read_h5(self, h5f):
        data = self.table_reader.read(h5f)
        if data is not None:
            self.set_data(self.table_reader.read(h5f))

    def resize(self, new_size):
        self.data.resize(new_size)

    def set_data(self, data):
        self.resize(data.size)
        np.copyto(self.data, data)
