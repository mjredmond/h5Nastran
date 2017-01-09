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

from ..abstract_table import AbstractTable
from .._main import register_table

import numpy as np


@register_table('CQUAD4')
class CQUAD4(AbstractTable):
    group = '/NASTRAN/INPUT/ELEMENT'
    table_id = 'CQUAD4'
    table_path = '%s/%s' % (group, table_id)

    class Format(IsDescription):
        EID = Int64Col(pos=1)
        PID = Int64Col(pos=2)
        GRID = Int64Col(shape=4, pos=3)
        THETA = Float64Col(pos=4)
        MCID = Int64Col(pos=5)
        ZOFFS = Float64Col(pos=6)
        TFLAG = Int64Col(pos=7)
        Ti = Float64Col(shape=4, pos=8)
        DOMAIN_ID = Int64Col(pos=9)

    @classmethod
    def _write_data(cls, h5f, table_data, h5table):
        table_row = h5table.row

        domain = cls.domain_count

        ids = sorted(table_data.keys())

        for _id in ids:

            # TODO: what to do about multiple definitions?
            data_i = table_data[_id][0].data
            data_i_get = data_i.get

            table_row['EID'] = data_i[1]
            table_row['PID'] = data_i_get(2, data_i[1])
            table_row['GRID'] = data_i[3:7]

            theta = data_i[7]
            mcid = 0

            if isinstance(theta, int):
                mcid = theta
                theta = np.nan
            elif theta is None:
                theta = 0.
                mcid = 0

            table_row['THETA'] = theta
            table_row['MCID'] = mcid

            table_row['ZOFFS'] = data_i_get(8, 0.)
            table_row['TFLAG'] = data_i_get(10, 0)

            ti = [
                data_i_get(11, 0.),
                data_i_get(12, 0.),
                data_i_get(13, 0.),
                data_i_get(14, 0.)
            ]

            table_row['Ti'] = ti

            table_row['DOMAIN_ID'] = domain

            table_row.append()

        h5f.flush()
