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
import tables

from .._abstract_table import AbstractTable


norm = np.linalg.norm


class CORD2Table(AbstractTable):

    group = '/NASTRAN/INPUT/COORDINATE'
    table_id = ''
    table_path = ''

    # class Format(IsDescription):
    #     CID = Int64Col(pos=1)
    #     RID = Int64Col(pos=2)
    #     A = Float64Col(shape=3, pos=3)
    #     B = Float64Col(shape=3, pos=4)
    #     C = Float64Col(shape=3, pos=5)
    #     DOMAIN_ID = Int64Col(pos=6)

    dtype = np.dtype([
        ('CID', np.int64),
        ('RID', np.int64),
        ('A', np.float64, (3,)),
        ('B', np.float64, (3,)),
        ('C', np.float64, (3,)),
        ('DOMAIN_ID', np.int64)
    ])

    Format = tables.descr_from_dtype(dtype)[0]

    @classmethod
    def _write_data(cls, h5f, table_data, h5table):
        table_row = h5table.row

        domain = cls.domain_count

        ids = sorted(table_data.keys())

        for _id in ids:

            # TODO: what to do about multiple definitions?
            data_i = table_data[_id][0].data
            data_i_get = data_i.get

            table_row['CID'] = data_i[1]
            table_row['RID'] = data_i_get(2, 0)
            table_row['A'] = data_i[3:6]
            table_row['B'] = data_i[6:9]
            table_row['C'] = data_i[9:12]
            table_row['DOMAIN_ID'] = domain

            table_row.append()

        h5f.flush()

    @classmethod
    def copy(cls):
        class _COPY(cls):
            pass

        return _COPY


class CORD2(object):

    table_reader = CORD2Table
    dtype = CORD2Table.dtype

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

            v3 = V3[i] = B[i] - A[i]
            V3[i] /= norm(v3)
            v3 = V3[i]

            v1 = V1[i] = C[i] - A[i]

            v2 = V2[i] = np.cross(v3, v1)
            V2[i] /= norm(v2)

            V1[i] = np.cross(v2, v3)

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

        return self.to_basic_coord(rid, xp)

