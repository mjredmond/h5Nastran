from __future__ import print_function, absolute_import
from six import iteritems, itervalues
from six.moves import range

from tables import IsDescription, Int64Col, Float64Col, StringCol
import tables

from .._abstract_table import AbstractTable
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
    def _write_data(cls, h5f, cards, h5table):

        table_row = h5table.row

        domain = cls.domain_count

        eids = sorted(cards.keys())

        for eid in eids:

            data = cards[eid]

            def _get_val(val, default):
                return default if val in (None, '') else val

            table_row['EID'] = data[1]
            table_row['PID'] = _get_val(data[2], data[1])
            table_row['GRID'] = data[3:7]

            theta = data[7]
            mcid = 0

            if isinstance(theta, int):
                mcid = theta
                theta = np.nan
            elif theta is None:
                theta = 0.
                mcid = 0

            table_row['THETA'] = theta
            table_row['MCID'] = mcid

            table_row['ZOFFS'] = _get_val(data[8], 0.)
            table_row['TFLAG'] = _get_val(data[10], 0)

            ti = [
                _get_val(data[11], 0.),
                _get_val(data[12], 0.),
                _get_val(data[13], 0.),
                _get_val(data[14], 0.)
            ]

            table_row['Ti'] = ti

            table_row['DOMAIN_ID'] = domain

            table_row.append()

        h5f.flush()


class CQUAD4(ElementCard):
    table_reader = Cquad4Table
    dtype = table_reader.dtype
    _id = 'EID'
