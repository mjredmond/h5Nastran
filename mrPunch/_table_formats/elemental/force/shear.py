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

from ...abstract_table import AbstractTable

from ..._main import register_table


@register_table('ELEMENT FORCES 4 SHEAR MATERIAL REAL OUTPUT')
@register_table('ELEMENT FORCES 4 SHEAR REAL OUTPUT')
class _Table_001(AbstractTable):

    group = '/NASTRAN/RESULT/ELEMENTAL/FORCE'
    table_id = 'SHEAR'
    table_path = '%s/%s' % (group, table_id)

    index_columns = ['EID']

    class Format(IsDescription):
        EID = Int64Col(pos=1)
        F14 = Float64Col(pos=2)
        F12 = Float64Col(pos=3)
        F21 = Float64Col(pos=4)
        F23 = Float64Col(pos=5)
        F32 = Float64Col(pos=6)
        F34 = Float64Col(pos=7)
        F43 = Float64Col(pos=8)
        F41 = Float64Col(pos=9)
        K1 = Float64Col(pos=10)
        SHR12 = Float64Col(pos=11)
        K2 = Float64Col(pos=12)
        SHR23 = Float64Col(pos=13)
        K3 = Float64Col(pos=14)
        SHR34 = Float64Col(pos=15)
        K4 = Float64Col(pos=16)
        SHR41 = Float64Col(pos=17)
        DOMAIN_ID = Int64Col(pos=18)

    @classmethod
    def _write_data(cls, h5f, table_data, h5table):
        table_row = h5table.row

        domain = cls.domain_count

        table_data = table_data.data

        for data_i in table_data:

            # data_i[1] = blank

            table_row['EID'] = data_i[0]
            table_row['F14'] = data_i[2]
            table_row['F12'] = data_i[3]
            table_row['F21'] = data_i[4]
            table_row['F23'] = data_i[5]
            table_row['F32'] = data_i[6]
            table_row['F34'] = data_i[7]
            table_row['F43'] = data_i[8]
            table_row['F41'] = data_i[9]
            table_row['K1'] = data_i[10]
            table_row['SHR12'] = data_i[11]
            table_row['K2'] = data_i[12]
            table_row['SHR23'] = data_i[13]
            table_row['K3'] = data_i[14]
            table_row['SHR34'] = data_i[15]
            table_row['K4'] = data_i[16]
            table_row['SHR41'] = data_i[17]
            table_row['DOMAIN_ID'] = domain

            table_row.append()

        h5f.flush()
