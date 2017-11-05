"""
Copyright (C) Michael James Redmond, Jr - All Rights Reserved
Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Michael James Redmond, Jr.
"""
from __future__ import print_function, absolute_import
from six import iteritems, iterkeys, itervalues
from six.moves import range

import numpy as np

norm = np.linalg.norm


class CordCard(object):

    table_reader = None
    dtype = None
    """:type: np.dtype"""

    _dtype = np.dtype([
        ('V1', np.float64, (3,)),
        ('V2', np.float64, (3,)),
        ('V3', np.float64, (3,))
    ])

    def __init__(self, bdf_data):
        self.bdf_data = bdf_data

        self.data = np.zeros(0, dtype=self.dtype)
        self._data = np.zeros(0, dtype=self._dtype)
        self.index = {}

        self._current_index = -1
        self._current_data_1 = None
        self._current_data_2 = None

    def read_h5(self, h5f):
        self.set_data(self.table_reader.read(h5f))

    def resize(self, new_size):
        self._current_index = -1
        self._current_data_1 = None
        self._current_data_2 = None

        self.data.resize(new_size)
        self._data.resize(new_size)

    def set_data(self, data):
        if data is None:
            return

        self.resize(data.size)

        np.copyto(self.data, data)

        self.update()

    def update(self):
        self.index.clear()

        cid = self.data['CID']
        A = self.data['A']
        B = self.data['B']
        C = self.data['C']

        V1 = self._data['V1']
        V2 = self._data['V2']
        V3 = self._data['V3']

        for i in range(self.data.size):
            self.index[cid[i]] = i

            v3 = B[i] - A[i]
            v3 /= norm(v3)

            v1 = C[i] - A[i]

            v2 = np.cross(v3, v1)
            v2 /= norm(v2)

            V1[i] = np.cross(v2, v3)
            V2[i] = v2
            V3[i] = v3

    def set_cid(self, cid):
        try:
            self._current_index = self.index[cid]
        except KeyError:
            raise ValueError('Unknown CID! %d' % cid)

        try:
            self._current_data_1 = self.data[self._current_index]
            self._current_data_2 = self._data[self._current_index]
        except IndexError:
            raise ValueError('CID %d not found in data!' % cid)

    def to_reference_coord(self, cid, x):
        self.set_cid(cid)

        data = self._current_data_1
        v1, v2, v3 = self._current_data_2

        xp = [np.dot(x, v1), np.dot(x, v2), np.dot(x, v3)]

        return xp + data[2]

    def to_basic_coord(self, cid, x):
        xp = self.to_reference_coord(cid, x)

        rid = self._current_data_1[1]

        if rid == 0:
            return xp

        return self.bdf_data.cord.to_basic_coord(rid, xp)
