"""
"""
from __future__ import print_function, absolute_import
from six import iteritems, itervalues
from six.moves import range

from ..._main import register_table

from tables import IsDescription, Int64Col, Float64Col, StringCol
import tables

from ...abstract_table import AbstractTable


@register_table('ELEMENT STRESSES 144 QUAD4C VONM REAL OUTPUT')
@register_table('ELEMENT STRESSES 144 QUAD4C VONM FIBER REAL OUTPUT')
@register_table('ELEMENT STRESSES 144 QUAD4C VONM BILIN REAL OUTPUT')
@register_table('ELEMENT STRESSES 144 QUAD4C VONM FIBER BILIN REAL OUTPUT')
class _Table_0001(AbstractTable):

    group = '/NASTRAN/RESULT/ELEMENTAL/STRESS'
    table_id = 'QUAD4_CN'
    table_path = '%s/%s' % (group, table_id)

    index_columns = ['EID']

    class Format(IsDescription):
        EID = Int64Col(pos=1)
        TERM = StringCol(4, pos=2)
        GRID = Int64Col(shape=5, pos=3)
        DIST = Float64Col(shape=(5, 2), pos=4)
        NORMAL_X = Float64Col(shape=(5, 2), pos=4)
        NORMAL_Y = Float64Col(shape=(5, 2), pos=5)
        SHEAR_XY = Float64Col(shape=(5, 2), pos=6)
        ANGLE = Float64Col(shape=(5, 2), pos=7)
        MAJOR = Float64Col(shape=(5, 2), pos=8)
        MINOR = Float64Col(shape=(5, 2), pos=9)
        VONM = Float64Col(shape=(5, 2), pos=10)
        DOMAIN_ID = Int64Col(pos=11)

    @classmethod
    def _write_data(cls, h5f, table_data, h5table):
        table_row = h5table.row

        domain = cls.domain_count

        table_data = table_data.data

        def slice_data(data, i1):
            return [
                (data[i1], data[i1+8]),
                (data[i1+17], data[i1+25]),
                (data[i1+34], data[i1+42]),
                (data[i1+51], data[i1+59]),
                (data[i1+68], data[i1+76]),
            ]

        for data_i in table_data:

            # data_i[1] = blank

            table_row['EID'] = data_i[0]
            table_row['TERM'] = data_i[2]
            table_row['GRID'] = [0, data_i[20], data_i[37], data_i[54], data_i[71]]
            table_row['DIST'] = slice_data(data_i, 4)
            table_row['NORMAL_X'] = slice_data(data_i, 5)
            table_row['NORMAL_Y'] = slice_data(data_i, 6)
            table_row['SHEAR_XY'] = slice_data(data_i, 7)
            table_row['ANGLE'] = slice_data(data_i, 8)
            table_row['MAJOR'] = slice_data(data_i, 9)
            table_row['MINOR'] = slice_data(data_i, 10)
            table_row['VONM'] = slice_data(data_i, 11)

            table_row['DOMAIN_ID'] = domain

            table_row.append()

        h5f.flush()


@register_table('ELEMENT STRAINS 144 QUAD4C VONM REAL OUTPUT')
@register_table('ELEMENT STRAINS 144 QUAD4C VONM FIBER REAL OUTPUT')
@register_table('ELEMENT STRAINS 144 QUAD4C VONM BILIN REAL OUTPUT')
@register_table('ELEMENT STRAINS 144 QUAD4C VONM FIBER BILIN REAL OUTPUT')
class _Table_0002(_Table_0001):
    group = '/NASTRAN/RESULT/ELEMENTAL/STRAIN'
    table_id = 'QUAD4_CN'
    table_path = '%s/%s' % (group, table_id)
