"""
"""
from __future__ import print_function, absolute_import
from six import iteritems, itervalues
from six.moves import range

from .._main import register_table

from tables import IsDescription, Int64Col, Float64Col, StringCol
import tables


from ..abstract_table import AbstractTable

import numpy as np


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
            b'': 0
        }

        eids_get = eids.get

        for data_i in table_data:

            table_row['ID'] = data_i[0]

            # data_i[1] = blank
            # data_i[4] = blank

            elname = data_i[3]

            eid = eids_get(data_i[2], data_i[2])

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

    @classmethod
    def _write_private_index(cls, h5f):
        table = cls.get_table(h5f)

        # noinspection PyProtectedMember
        col1 = table.cols._f_col(cls.index_columns[0])[:]

        if col1.size == 0:
            return

        col2 = table.cols._f_col(cls.index_columns[1])[:]
        col3 = table.cols._f_col('ELNAME')[:]

        data = np.empty((col1.size, 2), dtype=col1.dtype)
        data[:, 0] = col1

        eids = {
            b'F-OF-SPC': -1,
            b'F-OF-MPC': -2,
            b'APP-LOAD': -3,
            b'*TOTALS*': -4
        }

        eids_get = eids.get

        for i in range(col3.shape[0]):
            data[i, 1] = eids_get(col3[i].strip(), col2[i])

        h5f.create_array('/PRIVATE/INDEX' + cls.group, cls.table_id, obj=data, title=cls.results_type, createparents=True)