"""
Copyright (C) Michael James Redmond, Jr - All Rights Reserved
Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Michael James Redmond, Jr.
"""
from __future__ import print_function, absolute_import
from six import iteritems, itervalues
from six.moves import range

from tables import IsDescription, Int64Col, Float64Col, StringCol
import tables

from ...abstract_table import AbstractTable


class StrainEnergyTable(AbstractTable):

    group = '/NASTRAN/RESULT/ELEMENTAL/STRAIN_ENERGY'
    table_id = ''
    table_path = ''

    index_columns = ['ID']

    class Format(IsDescription):
        ID = Int64Col(pos=1)
        STRAIN_ENERGY = Float64Col(pos=2)
        PERCENT_OF_TOTAL = Float64Col(pos=3)
        DENSITY = Float64Col(pos=4)
        DOMAIN_ID = Int64Col(pos=5)

    @classmethod
    def _write_data(cls, h5f, table_data, h5table):
        table_row = h5table.row

        domain = cls.domain_count

        table_data = table_data.data

        for data_i in table_data:

            # print(data_i)

            table_row['ID'] = data_i[0]
            table_row['STRAIN_ENERGY'] = data_i[2]
            table_row['PERCENT_OF_TOTAL'] = data_i[3]
            table_row['DENSITY'] = data_i[4]
            table_row['DOMAIN_ID'] = domain

            table_row.append()

        h5f.flush()
