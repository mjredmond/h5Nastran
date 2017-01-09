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

from ..abstract_table import AbstractTable
from .._main import register_table

import numpy as np


@register_table('PSHELL')
class PSHELL(AbstractTable):
    group = '/NASTRAN/INPUT/PROPERTY'
    table_id = 'PSHELL'
    table_path = '%s/%s' % (group, table_id)

    class Format(IsDescription):
        PID = Int64Col(pos=1)
        MID1 = Int64Col(pos=2)
        T = Float64Col(pos=3)
        MID2 = Float64Col(pos=4)
        I = Float64Col(pos=5)
        MID3 = Int64Col(pos=6)
        TST = Float64Col(pos=7)
        NSM = Float64Col(pos=8)
        Z1 = Float64Col(pos=9)
        Z2 = Float64Col(pos=10)
        MID4 = Int64Col(pos=11)
        DOMAIN_ID = Int64Col(pos=12)

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
