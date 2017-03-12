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
from ._property import PropertyCard

import numpy as np


class PbarTable(AbstractTable):
    group = '/NASTRAN/INPUT/PROPERTY'
    table_id = 'PBAR'
    table_path = '%s/%s' % (group, table_id)

    dtype = np.dtype([
        ('PID', np.int64),
        ('MID', np.int64),
        ('A', np.float64),
        ('I1', np.float64),
        ('I2', np.float64),
        ('J', np.float64),
        ('NSM', np.float64),
        ('C1', np.float64),
        ('C2', np.float64),
        ('D1', np.float64),
        ('D2', np.float64),
        ('E1', np.float64),
        ('E2', np.float64),
        ('F1', np.float64),
        ('F2', np.float64),
        ('K1', np.float64),
        ('K2', np.float64),
        ('I12', np.float64),
        ('DOMAIN_ID', np.int64)
    ])

    Format = tables.descr_from_dtype(dtype)[0]

    @classmethod
    def _write_data(cls, h5f, table_data, h5table):
        table_row = h5table.row

        domain = cls.domain_count

        ids = sorted(map(int, table_data.keys()))

        for _id in ids:

            _id = str(_id)

            # TODO: what to do about multiple definitions?
            data_i = table_data[_id][0].data
            data_i_get = data_i.get

            table_row['PID'] = data_i[1]
            table_row['MID'] = data_i_get(2, -1)
            table_row['A'] = data_i_get(3, 0.)
            table_row['I1'] = data_i_get(4, 0.)
            table_row['I2'] = data_i_get(5, 0.)
            table_row['J'] = data_i_get(6, 0.)
            table_row['NSM'] = data_i_get(7, 0.)
            table_row['C1'] = data_i_get(9, 0.)
            table_row['C2'] = data_i_get(10, 0.)
            table_row['D1'] = data_i_get(11, 0.)
            table_row['D2'] = data_i_get(12, 0.)
            table_row['E1'] = data_i_get(13, 0.)
            table_row['E2'] = data_i_get(14, 0.)
            table_row['F1'] = data_i_get(15, 0.)
            table_row['F2'] = data_i_get(16, 0.)
            table_row['K1'] = data_i_get(17, 0.)
            table_row['K2'] = data_i_get(18, 0.)

            table_row['DOMAIN_ID'] = domain

            table_row.append()

        h5f.flush()


@register_card
class PBAR(PropertyCard):
    table_reader = PbarTable
    dtype = table_reader.dtype
