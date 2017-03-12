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
from ._cord import CordCard


norm = np.linalg.norm


class Cord2Table(AbstractTable):

    group = '/NASTRAN/INPUT/COORDINATE'
    table_id = ''
    table_path = ''

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

        ids = sorted(map(int, table_data.keys()))

        for _id in ids:

            _id = str(_id)

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


class Cord2(CordCard):
    table_reader = Cord2Table
    dtype = Cord2Table.dtype


