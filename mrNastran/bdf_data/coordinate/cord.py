from __future__ import print_function, absolute_import
from six import iteritems, iterkeys, itervalues
from six.moves import range


from .cord2c import CORD2C
from .cord2r import CORD2R
from .cord2rx import CORD2RX
from .cord2s import CORD2S


class Cord(object):
    def __init__(self, bdf_data):
        self.bdf_data = bdf_data

        self.cord2c = CORD2C(bdf_data)
        self.cord2r = CORD2R(bdf_data)
        self.cord2rx = CORD2RX(bdf_data)
        self.cord2s = CORD2S(bdf_data)

        self._cord = None

    def read_h5(self, h5f):
        self.cord2c.read_h5(h5f)
        self.cord2r.read_h5(h5f)
        self.cord2rx.read_h5(h5f)
        self.cord2s.read_h5(h5f)
