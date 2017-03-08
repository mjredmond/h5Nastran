"""
Copyright (C) Michael James Redmond, Jr - All Rights Reserved
Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Michael James Redmond, Jr.
"""
from __future__ import print_function, absolute_import
from six import iteritems, iterkeys, itervalues
from six.moves import range


from .._cards import register_card_only

from .cord2c import CORD2C
from .cord2r import CORD2R
from .cord2rx import CORD2RX
from .cord2s import CORD2S


@register_card_only
class CORD(object):
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

    def set_cid(self, cid):
        try:
            self.cord2c.set_cid(cid)
            self._cord = self.cord2c
        except ValueError:
            pass

        try:
            self.cord2r.set_cid(cid)
            self._cord = self.cord2r
        except ValueError:
            pass

        try:
            self.cord2s.set_cid(cid)
            self._cord = self.cord2s
        except ValueError:
            pass

        try:
            self.cord2rx.set_cid(cid)
            self._cord = self.cord2rx
        except ValueError:
            pass

        raise ValueError('CID %d does not exist!' % cid)

    def to_reference_coord(self, cid, x):
        self.set_cid(cid)
        self._cord.to_reference_coord(cid, x)

    def to_basic_coord(self, cid, x):
        self.set_cid(cid)
        self._cord.to_basic_coord(cid, x)