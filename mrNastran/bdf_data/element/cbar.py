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
from ._element import Element

import numpy as np


class CbarTable(AbstractTable):

    group = '/NASTRAN/INPUT/ELEMENT'
    table_id = 'CBAR'
    table_path = '%s/%s' % (group, table_id)

    dtype = np.dtype([
        ('EID', np.int64),
        ('PID', np.int64),
        ('GRID', np.int64, (2,)),
        ('X', np.float64, (3,)),
        ('G0', np.int64),
        ('OFFT', 'S3'),
        ('PA', np.int64),
        ('PB', np.int64),
        ('WA', np.float64, (3,)),
        ('WB', np.float64, (3,)),
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

            table_row['EID'] = data_i[1]
            table_row['PID'] = data_i_get(2, data_i[1])
            table_row['GRID'] = data_i[3:5]

            tmp = data_i[5:8]

            if tmp.count(None) == 3:
                table_row['G0'] = data_i[3]
                table_row['X'] = 0.
            elif isinstance(data_i[5], int):
                table_row['G0'] = data_i[5]
            else:
                table_row['G0'] = -1
                table_row['X'] = data_i[5:8]

            table_row['OFFT'] = data_i_get(8, '')
            table_row['PA'] = data_i_get(9, 0)
            table_row['PB'] = data_i_get(10, 0)

            wa = (data_i_get(11, 0.), data_i_get(12, 0.), data_i_get(13, 0.))
            wb = (data_i_get(14, 0.), data_i_get(15, 0.), data_i_get(16, 0.))

            table_row['WA'] = wa
            table_row['WB'] = wb

            table_row['DOMAIN_ID'] = domain

            table_row.append()

        h5f.flush()


@register_card
class CBAR(Element):
    table_reader = CbarTable
    dtype = table_reader.dtype
