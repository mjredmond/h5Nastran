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
from .._cards import register_card


class GridTable(AbstractTable):

    group = '/NASTRAN/INPUT/NODE'
    table_id = 'GRID'
    table_path = '%s/%s' % (group, table_id)

    dtype = np.dtype([
        ('ID', np.int64),
        ('CP', np.int64),
        ('X', np.float64, (3,)),
        ('CD', np.int64),
        ('PS', np.int64),
        ('SEID', np.int64),
        ('DOMAIN_ID', np.int64)
    ])

    Format = tables.descr_from_dtype(dtype)[0]

    @classmethod
    def _write_data(cls, h5f, table_data, h5table):
        table_row = h5table.row

        domain = cls.domain_count

        grid_ids = sorted(map(int, table_data.keys()))

        for grid_id in grid_ids:

            grid_id = str(grid_id)

            # TODO: what to do about multiple definitions?
            data_i = table_data[grid_id][0].data
            data_i_get = data_i.get

            _data_i = [data_i[1], data_i[2], data_i[3:6], data_i_get(7), data_i_get(8), data_i_get(9)]

            def _get_data(data_):
                return data_ if data_ is not None else 0

            table_row['ID'] = _data_i[0]
            table_row['CP'] = _get_data(_data_i[1])
            table_row['X'] = _data_i[2]
            table_row['CD'] = _get_data(_data_i[3])
            table_row['PS'] = _get_data(_data_i[4])
            table_row['SEID'] = _get_data(_data_i[5])
            table_row['DOMAIN_ID'] = domain

            table_row.append()

        h5f.flush()


@register_card
class GRID(object):

    table_reader = GridTable
    dtype = GridTable.dtype

    def __init__(self, bdf_data):
        self.bdf_data = bdf_data

        self.data = np.zeros(0, dtype=self.dtype)
        self.index = {}

        self._current_index = -1
        self._current_data = None

    def read_h5(self, h5f):
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

        nid = self.data['ID']

        for i in range(self.data.size):
            self.index[nid[i]] = i

    def set_nid(self, nid):
        try:
            self._current_index = self.index[nid]
        except KeyError:
            raise ValueError('Unknown NID! %d' % nid)

        try:
            self._current_data = self.data[self._current_index]
        except IndexError:
            raise ValueError('NID %d not found in data!' % nid)

    def to_basic(self, nid, convert_data=False):
        self.set_nid(nid)

        x = self._current_data['X']
        cid = self._current_data['CP']

        xb = self.bdf_data.cord.to_basic_coord(cid, x)

        if convert_data:
            x[:] = xb

        return xb

    def all_to_basic(self, convert_data=False):

        if convert_data:
            data = self.data
        else:
            data = np.array(self.data, dtype=self.dtype)

        x = data['X']
        cid = data['CP']

        to_basic_coord = self.bdf_data.cord.to_basic_coord

        for i in range(data.shape[0]):
            _cid = cid[i]
            if _cid == 0:
                continue

            # print(id[i], _cid, x[i])
            x[i] = to_basic_coord(_cid, x[i])
            # print(x[i])
            cid[i] = 0

        return data
