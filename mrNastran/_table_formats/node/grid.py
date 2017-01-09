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

from tables import IsDescription, Int64Col, Float64Col, StringCol, BoolCol
import tables

from ..abstract_table import AbstractTable


@register_table('GRID')
class _Table_0001(AbstractTable):

    group = '/NASTRAN/INPUT/NODE'
    table_id = 'GRID'
    table_path = '%s/%s' % (group, table_id)

    class Format(IsDescription):
        ID = Int64Col(pos=1)
        CP = Int64Col(pos=2)
        X = Float64Col(shape=3, pos=2)
        CD = Int64Col(pos=3)
        PS = Int64Col(pos=4)
        SEID = Int64Col(pos=5)
        DOMAIN_ID = Int64Col(pos=6)

    class FillFormat(IsDescription):
        ID = BoolCol(pos=1)
        CP = BoolCol(pos=2)
        X = BoolCol(pos=2)
        CD = BoolCol(pos=3)
        PS = BoolCol(pos=4)
        SEID = BoolCol(pos=5)

    @classmethod
    def _write_data(cls, h5f, table_data, h5table):
        data_table, fill_table = h5table

        table_row = data_table.row
        fill_row = fill_table.row

        domain = cls.domain_count

        grid_ids = sorted(table_data.keys())

        _keys = ['ID', 'CP', 'X', 'CD', 'PS', 'SEID']

        for grid_id in grid_ids:

            # TODO: what to do about multiple definitions?
            data_i = table_data[grid_id][0].data
            data_i_get = data_i.get

            _data_i = [data_i[1], data_i[2], data_i[3:6], data_i_get(7), data_i_get(8), data_i_get(9)]

            table_row['ID'] = _data_i[0]
            table_row['CP'] = _data_i[1]
            table_row['X'] = _data_i[2]
            table_row['CD'] = _data_i[3] if _data_i[3] is not None else 0
            table_row['PS'] = _data_i[4] if _data_i[4] is not None else 0
            table_row['SEID'] = _data_i[5] if _data_i[5] is not None else 0
            table_row['DOMAIN_ID'] = domain

            table_row.append()

            for i in range(len(_keys)):
                key = _keys[i]
                _data = _data_i[i]

                if _data is None:
                    fill_row[key] = False
                else:
                    fill_row[key] = True

            fill_row.append()

        h5f.flush()
