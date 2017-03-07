"""
Copyright (C) Michael James Redmond, Jr - All Rights Reserved
Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Michael James Redmond, Jr.
"""
from __future__ import print_function, absolute_import
from six import iteritems, itervalues
from six.moves import range

from tables import IsDescription, Int64Col, Float64Col, StringCol
import tables

from .._abstract_table import AbstractTable
from .._cards import register_card

import numpy as np


class PSHELLTable(AbstractTable):
    group = '/NASTRAN/INPUT/PROPERTY'
    table_id = 'PSHELL'
    table_path = '%s/%s' % (group, table_id)

    dtype = np.dtype([
        ('PID', np.int64),
        ('MID1', np.int64),
        ('T', np.float64),
        ('MID2', np.int64),
        ('I', np.float64),
        ('MID3', np.int64),
        ('TST', np.float64),
        ('NSM', np.float64),
        ('Z1', np.float64),
        ('Z2', np.float64),
        ('MID4', np.int64),
        ('DOMAIN_ID', np.int64)
    ])

    Format = tables.descr_from_dtype(dtype)[0]

    # class Format(IsDescription):
    #     PID = Int64Col(pos=1)
    #     MID1 = Int64Col(pos=2)
    #     T = Float64Col(pos=3)
    #     MID2 = Float64Col(pos=4)
    #     I = Float64Col(pos=5)
    #     MID3 = Int64Col(pos=6)
    #     TST = Float64Col(pos=7)
    #     NSM = Float64Col(pos=8)
    #     Z1 = Float64Col(pos=9)
    #     Z2 = Float64Col(pos=10)
    #     MID4 = Int64Col(pos=11)
    #     DOMAIN_ID = Int64Col(pos=12)

    @classmethod
    def _write_data(cls, h5f, table_data, h5table):
        table_row = h5table.row

        domain = cls.domain_count

        ids = sorted(table_data.keys())

        for _id in ids:

            # TODO: what to do about multiple definitions?
            data_i = table_data[_id][0].data
            data_i_get = data_i.get

            table_row['PID'] = data_i[1]
            table_row['MID1'] = data_i_get(2, -1)
            table_row['T'] = data_i_get(3, np.nan)
            table_row['MID2'] = data_i_get(4, -1)
            table_row['I'] = data_i_get(5, 1.)
            table_row['MID3'] = data_i_get(6, -1)
            table_row['TST'] = data_i_get(7, 0.833333)
            table_row['NSM'] = data_i_get(8, 0.)
            table_row['Z1'] = data_i_get(9, 0.)
            table_row['Z2'] = data_i_get(10, 0.)
            table_row['MID4'] = data_i_get(11, -1)

            table_row['DOMAIN_ID'] = domain

            table_row.append()

        h5f.flush()


@register_card
class PSHELL(object):

    table_reader = PSHELLTable
    dtype = table_reader.dtype

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
