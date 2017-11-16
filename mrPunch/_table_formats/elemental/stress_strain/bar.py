"""
"""
from __future__ import print_function, absolute_import
from six import iteritems, itervalues
from six.moves import range

from ..._main import register_table

from tables import IsDescription, Int64Col, Float64Col, StringCol
import tables

from ...abstract_table import AbstractTable


@register_table('ELEMENT STRESSES 34 BAR REAL OUTPUT')
class _Table_0001(AbstractTable):

    group = '/NASTRAN/RESULT/ELEMENTAL/STRESS'
    table_id = 'BAR'
    table_path = '%s/%s' % (group, table_id)

    index_columns = ['EID']

    class Format(IsDescription):
        EID = Int64Col(pos=1)
        SA1 = Float64Col(pos=2)
        SA2 = Float64Col(pos=2)
        SA3 = Float64Col(pos=3)
        SA4 = Float64Col(pos=4)
        AX = Float64Col(pos=5)
        SA_MAX = Float64Col(pos=6)
        SA_MIN = Float64Col(pos=7)
        MS_T = Float64Col(pos=8)
        SB1 = Float64Col(pos=9)
        SB2 = Float64Col(pos=10)
        SB3 = Float64Col(pos=11)
        SB4 = Float64Col(pos=12)
        SB_MAX = Float64Col(pos=13)
        SB_MIN = Float64Col(pos=14)
        MS_C = Float64Col(pos=15)
        DOMAIN_ID = Int64Col(pos=16)

    @classmethod
    def _write_data(cls, h5f, table_data, h5table):
        table_row = h5table.row

        domain = cls.domain_count

        table_data = table_data.data

        for data_i in table_data:

            # data_i[1] = blank

            table_row['EID'] = data_i[0]
            table_row['SA1'] = data_i[2]
            table_row['SA2'] = data_i[3]
            table_row['SA3'] = data_i[4]
            table_row['SA4'] = data_i[5]
            table_row['AX'] = data_i[6]
            table_row['SA_MAX'] = data_i[7]
            table_row['SA_MIN'] = data_i[8]
            table_row['MS_T'] = data_i[9]
            table_row['SB1'] = data_i[10]
            table_row['SB2'] = data_i[11]
            table_row['SB3'] = data_i[12]
            table_row['SB4'] = data_i[13]
            table_row['SB_MAX'] = data_i[14]
            table_row['SB_MIN'] = data_i[15]
            table_row['MS_C'] = data_i[16]
            table_row['DOMAIN_ID'] = domain

            table_row.append()

        h5f.flush()


@register_table('ELEMENT STRAINS 34 BAR REAL OUTPUT')
class _Table_0002(_Table_0001):
    group = '/NASTRAN/RESULT/ELEMENTAL/STRAIN'
    table_id = 'BAR'
    table_path = '%s/%s' % (group, table_id)
