"""
"""
from __future__ import print_function, absolute_import
from six import iteritems, itervalues
from six.moves import range

from tables import IsDescription, Int64Col, Float64Col, StringCol
import tables

from .._abstract_table import AbstractTable
from .._cards import register_card
from ._element import ElementCard

import numpy as np


class Cquad4Table(AbstractTable):

    group = '/NASTRAN/INPUT/ELEMENT'
    table_id = 'CQUAD4'
    table_path = '%s/%s' % (group, table_id)

    dtype = np.dtype([
        ('EID', np.int64),
        ('PID', np.int64),
        ('GRID', np.int64, (4,)),
        ('THETA', np.float64),
        ('MCID', np.int64),
        ('ZOFFS', np.float64),
        ('TFLAG', np.int64),
        ('Ti', np.float64, (4,)),
        ('DOMAIN_ID', np.int64)
    ])

    Format = tables.descr_from_dtype(dtype)[0]

    @classmethod
    def _write_data(cls, h5f, table_data, h5table):
        table_row = h5table.row

        domain = cls.domain_count

        ids = sorted(map(int, table_data.keys()))

        for _id in ids:

            _id = str(_id)

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


@register_card
class CQUAD4(ElementCard):
    table_reader = Cquad4Table
    dtype = table_reader.dtype
