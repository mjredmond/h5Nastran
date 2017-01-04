"""
Copyright (C) Michael James Redmond, Jr - All Rights Reserved
Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Michael James Redmond, Jr.
"""
from __future__ import print_function, absolute_import
from six import iteritems, itervalues
from six.moves import range

from ..._main import register_table

from tables import IsDescription, Int64Col, Float64Col, StringCol
import tables

from ...abstract_table import AbstractTable


@register_table('ELEMENT FORCES 34 BAR REAL OUTPUT')
class _Table_0001(AbstractTable):

    group = '/NASTRAN/RESULT/ELEMENTAL/FORCE'
    table_id = 'BAR'
    table_path = '%s/%s' % (group, table_id)

    index_columns = ['EID']

    class Format(IsDescription):
        EID = Int64Col(pos=1)
        M1A = Float64Col(pos=2)
        M2A = Float64Col(pos=2)
        M1B = Float64Col(pos=3)
        M2B = Float64Col(pos=4)
        SHR1 = Float64Col(pos=5)
        SHR2 = Float64Col(pos=6)
        AX = Float64Col(pos=7)
        T = Float64Col(pos=8)
        DOMAIN_ID = Int64Col(pos=9)

    @classmethod
    def _write_data(cls, h5f, table_data, h5table):
        table_row = h5table.row

        domain = cls.domain_count

        table_data = table_data.data

        for data_i in table_data:

            # data_i[1] = blank

            table_row['EID'] = data_i[0]
            table_row['M1A'] = data_i[2]
            table_row['M2A'] = data_i[3]
            table_row['M1B'] = data_i[4]
            table_row['M2B'] = data_i[5]
            table_row['SHR1'] = data_i[6]
            table_row['SHR2'] = data_i[7]
            table_row['AX'] = data_i[8]
            table_row['T'] = data_i[9]
            table_row['DOMAIN_ID'] = domain

            table_row.append()

        h5f.flush()
