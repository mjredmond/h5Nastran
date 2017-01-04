"""
Copyright (C) Michael James Redmond, Jr - All Rights Reserved
Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Michael James Redmond, Jr.
"""
from __future__ import print_function, absolute_import
from six import iteritems, itervalues
from six.moves import range

from .._main import register_table

from tables import IsDescription, Int64Col, Float64Col, StringCol
import tables


from ..abstract_table import AbstractTable


@register_table('GRID POINT FORCE BALANCE REAL OUTPUT')
class _Table_0001(AbstractTable):

    group = '/NASTRAN/RESULT/NODAL'
    table_id = 'GRID_FORCE'
    table_path = '%s/%s' % (group, table_id)

    index_columns = ['ID', 'EID']

    class Format(IsDescription):
        ID = Int64Col(pos=1)
        EID = Int64Col(pos=2)
        ELNAME = StringCol(18, pos=3)
        F1 = Float64Col(pos=4)
        F2 = Float64Col(pos=5)
        F3 = Float64Col(pos=6)
        M1 = Float64Col(pos=7)
        M2 = Float64Col(pos=8)
        M3 = Float64Col(pos=9)
        DOMAIN_ID = Int64Col(pos=10)

    @classmethod
    def _write_data(cls, h5f, table_data, h5table):
        table_row = h5table.row

        domain = cls.domain_count

        table_data = table_data.data

        eids = {
            b'F-OF-SPC': -1,
            b'F-OF-MPC': -2,
            b'APP-LOAD': -3,
            b'*TOTALS*': -4
        }

        eids_get = eids.get

        for data_i in table_data:

            table_row['ID'] = data_i[0]

            # data_i[1] = blank
            # data_i[4] = blank

            elname = data_i[3]

            eid = eids_get(elname, data_i[2])

            table_row['EID'] = eid
            table_row['ELNAME'] = elname
            table_row['F1'] = data_i[5]
            table_row['F2'] = data_i[6]
            table_row['F3'] = data_i[7]
            table_row['M1'] = data_i[8]
            table_row['M2'] = data_i[9]
            table_row['M3'] = data_i[10]
            table_row['DOMAIN_ID'] = domain

            table_row.append()

        h5f.flush()
