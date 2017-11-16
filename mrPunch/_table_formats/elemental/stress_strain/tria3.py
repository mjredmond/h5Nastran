"""
"""
from __future__ import print_function, absolute_import
from six import iteritems, itervalues
from six.moves import range

from ..._main import register_table

from tables import IsDescription, Int64Col, Float64Col, StringCol
import tables

from ...abstract_table import AbstractTable


@register_table('ELEMENT STRESSES 74 TRIA3 VONM REAL OUTPUT')
@register_table('ELEMENT STRESSES 74 TRIA3 VONM FIBER REAL OUTPUT')
class _Table_0001(AbstractTable):

    group = '/NASTRAN/RESULT/ELEMENTAL/STRESS'
    table_id = 'TRIA3'
    table_path = '%s/%s' % (group, table_id)

    index_columns = ['EID']

    class Format(IsDescription):
        EID = Int64Col(pos=1)
        DIST = Float64Col(shape=2, pos=2)
        NORMAL_X = Float64Col(shape=2, pos=3)
        NORMAL_Y = Float64Col(shape=2, pos=4)
        SHEAR_XY = Float64Col(shape=2, pos=5)
        ANGLE = Float64Col(shape=2, pos=6)
        MAJOR = Float64Col(shape=2, pos=7)
        MINOR = Float64Col(shape=2, pos=8)
        VONM = Float64Col(shape=2, pos=9)
        DOMAIN_ID = Int64Col(pos=10)

    @classmethod
    def _write_data(cls, h5f, table_data, h5table):
        table_row = h5table.row

        domain = cls.domain_count

        table_data = table_data.data

        for data_i in table_data:

            # data_i[1] = blank

            table_row['EID'] = data_i[0]
            table_row['DIST'] = data_i[2:18:8]
            table_row['NORMAL_X'] = data_i[3:19:8]
            table_row['NORMAL_Y'] = data_i[4:20:8]
            table_row['SHEAR_XY'] = data_i[5:21:8]
            table_row['ANGLE'] = data_i[6:22:8]
            table_row['MAJOR'] = data_i[7:23:8]
            table_row['MINOR'] = data_i[8:24:8]
            table_row['VONM'] = data_i[9:25:8]
            table_row['DOMAIN_ID'] = domain

            table_row.append()

        h5f.flush()


@register_table('ELEMENT STRAINS 74 TRIA3 VONM REAL OUTPUT')
@register_table('ELEMENT STRAINS 74 TRIA3 VONM FIBER REAL OUTPUT')
class _Table_0002(_Table_0001):
    group = '/NASTRAN/RESULT/ELEMENTAL/STRAIN'
    table_id = 'TRIA3'
    table_path = '%s/%s' % (group, table_id)
