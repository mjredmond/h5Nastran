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


class PshellTable(AbstractTable):
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
class PSHELL(PropertyCard):
    table_reader = PshellTable
    dtype = table_reader.dtype
