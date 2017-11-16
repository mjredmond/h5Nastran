"""
"""
from __future__ import print_function, absolute_import
from six import iteritems, itervalues
from six.moves import range

from tables import IsDescription, Int64Col, Float64Col, StringCol
import tables

from ...abstract_table import AbstractTable


class ShellTable(AbstractTable):

    group = '/NASTRAN/RESULT/ELEMENTAL/FORCE'
    table_id = ''
    table_path = ''

    index_columns = ['EID']

    class Format(IsDescription):
        EID = Int64Col(pos=1)
        FX = Float64Col(pos=2)
        FY = Float64Col(pos=3)
        FXY = Float64Col(pos=4)
        MX = Float64Col(pos=5)
        MY = Float64Col(pos=6)
        MXY = Float64Col(pos=7)
        QX = Float64Col(pos=8)
        QY = Float64Col(pos=9)
        DOMAIN_ID = Int64Col(pos=10)

    @classmethod
    def _write_data(cls, h5f, table_data, h5table):
        table_row = h5table.row

        domain = cls.domain_count

        table_data = table_data.data

        for data_i in table_data:

            # data_i[1] = blank

            table_row['EID'] = data_i[0]
            table_row['FX'] = data_i[2]
            table_row['FY'] = data_i[3]
            table_row['FXY'] = data_i[4]
            table_row['MX'] = data_i[5]
            table_row['MY'] = data_i[6]
            table_row['MXY'] = data_i[7]
            table_row['QX'] = data_i[8]
            table_row['QY'] = data_i[9]
            table_row['DOMAIN_ID'] = domain

            table_row.append()

        h5f.flush()
