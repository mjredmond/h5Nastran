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


@register_table('ELEMENT FORCES 144 QUAD4C BILIN REAL OUTPUT')
@register_table('ELEMENT FORCES 144 QUAD4C REAL OUTPUT')
class _Table_0001(AbstractTable):

    group = '/NASTRAN/RESULT/ELEMENTAL/FORCE'
    table_id = 'QUAD4_CN'
    table_path = '%s/%s' % (group, table_id)

    # table_index = TableIndex()
    # domains = TableIndex()

    index_columns = ['EID']

    class Format(IsDescription):
        EID = Int64Col(pos=1)
        TERM = StringCol(4, pos=2)
        GRID = Int64Col(shape=5, pos=3)
        FX = Float64Col(shape=5, pos=4)
        FY = Float64Col(shape=5, pos=5)
        FXY = Float64Col(shape=5, pos=6)
        MX = Float64Col(shape=5, pos=7)
        MY = Float64Col(shape=5, pos=8)
        MXY = Float64Col(shape=5, pos=9)
        QX = Float64Col(shape=5, pos=10)
        QY = Float64Col(shape=5, pos=11)
        DOMAIN_ID = Int64Col(pos=12)

    @classmethod
    def _write_data(cls, h5f, table_data, h5table):
        table_row = h5table.row

        domain = cls.domain_count

        table_data = table_data.data

        for data_i in table_data:

            # data_i[1] = blank

            table_row['EID'] = data_i[0]
            table_row['TERM'] = data_i[2]
            table_row['GRID'] = [0, data_i[12], data_i[21], data_i[30], data_i[39]]
            table_row['FX'] = [data_i[4], data_i[13], data_i[22], data_i[31], data_i[40]]
            table_row['FY'] = [data_i[5], data_i[14], data_i[23], data_i[32], data_i[41]]
            table_row['FXY'] = [data_i[6], data_i[15], data_i[24], data_i[33], data_i[42]]
            table_row['MX'] = [data_i[7], data_i[16], data_i[25], data_i[34], data_i[43]]
            table_row['MY'] = [data_i[8], data_i[17], data_i[26], data_i[35], data_i[44]]
            table_row['MXY'] = [data_i[9], data_i[18], data_i[27], data_i[36], data_i[45]]
            table_row['QX'] = [data_i[10], data_i[19], data_i[28], data_i[37], data_i[46]]
            table_row['QY'] = [data_i[11], data_i[20], data_i[29], data_i[38], data_i[47]]

            table_row['DOMAIN_ID'] = domain

            table_row.append()

        h5f.flush()
