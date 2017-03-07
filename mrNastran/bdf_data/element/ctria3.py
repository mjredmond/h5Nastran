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


class CTRIA3Table(AbstractTable):

    group = '/NASTRAN/INPUT/ELEMENT'
    table_id = 'CTRIA3'
    table_path = '%s/%s' % (group, table_id)

    dtype = np.dtype([
        ('EID', np.int64),
        ('PID', np.int64),
        ('GRID', np.int64, (3,)),
        ('THETA', np.float64),
        ('MCID', np.int64),
        ('ZOFFS', np.float64),
        ('TFLAG', np.int64),
        ('Ti', np.float64, (3,)),
        ('DOMAIN_ID', np.int64)
    ])

    Format = tables.descr_from_dtype(dtype)[0]

    # class Format(IsDescription):
    #     EID = Int64Col(pos=1)
    #     PID = Int64Col(pos=2)
    #     GRID = Int64Col(shape=3, pos=3)
    #     THETA = Float64Col(pos=4)
    #     MCID = Int64Col(pos=5)
    #     ZOFFS = Float64Col(pos=6)
    #     TFLAG = Int64Col(pos=7)
    #     Ti = Float64Col(shape=3, pos=8)
    #     DOMAIN_ID = Int64Col(pos=9)

    @classmethod
    def _write_data(cls, h5f, table_data, h5table):
        table_row = h5table.row

        domain = cls.domain_count

        ids = sorted(table_data.keys())

        for _id in ids:

            # TODO: what to do about multiple definitions?
            data_i = table_data[_id][0].data
            data_i_get = data_i.get

            table_row['EID'] = data_i[1]
            table_row['PID'] = data_i_get(2, data_i[1])
            table_row['GRID'] = data_i[3:6]

            theta = data_i[6]
            mcid = 0

            if isinstance(theta, int):
                mcid = theta
                theta = np.nan
            elif theta is None:
                theta = 0.
                mcid = 0

            table_row['THETA'] = theta
            table_row['MCID'] = mcid

            table_row['ZOFFS'] = data_i_get(7, 0.)
            table_row['TFLAG'] = data_i_get(10, 0)

            ti = [
                data_i_get(11, 0.),
                data_i_get(12, 0.),
                data_i_get(13, 0.)
            ]

            table_row['Ti'] = ti

            table_row['DOMAIN_ID'] = domain

            table_row.append()

        h5f.flush()


@register_card
class CTRIA3(object):
    table_reader = CTRIA3Table
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

        eid = self.data['EID']

        for i in range(self.data.size):
            self.index[eid[i]] = i

    def set_eid(self, eid):
        try:
            self._current_index = self.index[eid]
        except KeyError:
            raise ValueError('Unknown EID! %d' % eid)

        try:
            self._current_data = self.data[self._current_index]
        except IndexError:
            raise ValueError('EID %d not found in data!' % eid)