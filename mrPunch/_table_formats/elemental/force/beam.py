"""
"""
from __future__ import print_function, absolute_import
from six import iteritems, itervalues
from six.moves import range

from ..._main import register_table

from tables import IsDescription, Int64Col, Float64Col, StringCol
import tables

from ...abstract_table import AbstractTable


@register_table('ELEMENT FORCES 2 BEAM REAL OUTPUT')
class _Table_0001(AbstractTable):

    group = '/NASTRAN/RESULT/ELEMENTAL/FORCE'
    table_id = 'BEAM'
    table_path = '%s/%s' % (group, table_id)

    index_columns = ['EID']

    class Format(IsDescription):
        EID = Int64Col(pos=1)
        GRID = Int64Col(shape=11, pos=2)
        DIST = Float64Col(shape=11, pos=3)
        M1 = Float64Col(shape=11, pos=4)
        M2 = Float64Col(shape=11, pos=5)
        SHR1 = Float64Col(shape=11, pos=6)
        SHR2 = Float64Col(shape=11, pos=7)
        AX = Float64Col(shape=11, pos=8)
        TT = Float64Col(shape=11, pos=9)
        WT = Float64Col(shape=11, pos=10)
        DOMAIN_ID = Int64Col(pos=11)

    @classmethod
    def _write_data(cls, h5f, table_data, h5table):
        table_row = h5table.row

        domain = cls.domain_count

        table_data = table_data.data

        for data_i in table_data:

            # data_i[1] = blank

            table_row['EID'] = data_i[0]

            table_row['GRID'] = data_i[2:101:9]
            table_row['DIST'] = data_i[3:102:9]
            table_row['M1'] = data_i[4:103:9]
            table_row['M2'] = data_i[5:104:9]
            table_row['SHR1'] = data_i[6:105:9]
            table_row['SHR2'] = data_i[7:106:9]
            table_row['AX'] = data_i[8:107:9]
            table_row['TT'] = data_i[9:108:9]
            table_row['WT'] = data_i[10:109:9]

            table_row['DOMAIN_ID'] = domain

            table_row.append()

        h5f.flush()
