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


@register_table('ELEMENT STRESSES 2 BEAM REAL OUTPUT')
class _Table_0001(AbstractTable):

    group = '/NASTRAN/RESULT/ELEMENTAL/STRESS'
    table_id = 'BEAM'
    table_path = '%s/%s' % (group, table_id)

    index_columns = ['EID']

    class Format(IsDescription):
        EID = Int64Col(pos=1)
        GRID = Int64Col(shape=11, pos=2)
        DIST = Float64Col(shape=11, pos=3)
        SXC = Float64Col(shape=11, pos=4)
        SXD = Float64Col(shape=11, pos=5)
        SXE = Float64Col(shape=11, pos=6)
        SXF = Float64Col(shape=11, pos=7)
        S_MAX = Float64Col(shape=11, pos=8)
        S_MIN = Float64Col(shape=11, pos=9)
        MS_T = Float64Col(shape=11, pos=10)
        MS_C = Float64Col(shape=11, pos=11)
        DOMAIN_ID = Int64Col(pos=12)

    @classmethod
    def _write_data(cls, h5f, table_data, h5table):
        table_row = h5table.row

        domain = cls.domain_count

        table_data = table_data.data

        for data_i in table_data:

            # data_i[1] = blank

            table_row['EID'] = data_i[0]

            table_row['GRID'] = data_i[2:112:10]
            table_row['DIST'] = data_i[3:113:10]
            table_row['SXC'] = data_i[4:114:10]
            table_row['SXD'] = data_i[5:115:10]
            table_row['SXE'] = data_i[6:116:10]
            table_row['SXF'] = data_i[7:117:10]
            table_row['S_MAX'] = data_i[8:118:10]
            table_row['S_MIN'] = data_i[9:119:10]
            table_row['MS_T'] = data_i[10:120:10]
            table_row['MS_C'] = data_i[11:121:10]

            table_row['DOMAIN_ID'] = domain

            table_row.append()

        h5f.flush()


@register_table('ELEMENT STRAINS 2 BEAM REAL OUTPUT')
class _Table_0002(_Table_0001):
    group = '/NASTRAN/RESULT/ELEMENTAL/STRAIN'
    table_id = 'BEAM'
    table_path = '%s/%s' % (group, table_id)
