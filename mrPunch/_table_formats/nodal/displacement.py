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


@register_table('DISPLACEMENTS REAL OUTPUT')
class _Table_0001(AbstractTable):

    group = '/NASTRAN/RESULT/NODAL'
    table_id = 'DISPLACEMENT'
    table_path = '%s/%s' % (group, table_id)

    index_columns = ['ID']

    class Format(IsDescription):
        ID = Int64Col(pos=1)
        VALUE = Float64Col(shape=6, pos=2)
        DOMAIN_ID = Int64Col(pos=3)

    @classmethod
    def _write_data(cls, h5f, table_data, h5table):
        table_row = h5table.row

        domain = cls.domain_count

        table_data = table_data.data

        for data_i in table_data:

            table_row['ID'] = data_i[0]
            table_row['VALUE'] = data_i[2:8]
            table_row['DOMAIN_ID'] = domain

            table_row.append()

        h5f.flush()
