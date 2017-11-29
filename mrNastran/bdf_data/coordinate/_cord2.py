from __future__ import print_function, absolute_import
from six import iteritems, iterkeys, itervalues
from six.moves import range

import numpy as np
import tables

from .._abstract_table import AbstractTable
from ._cord import CordCard


norm = np.linalg.norm


class Cord2Table(AbstractTable):

    group = '/NASTRAN/INPUT/COORDINATE'
    table_id = ''
    table_path = ''

    dtype = np.dtype([
        ('CID', np.int64),
        ('RID', np.int64),
        ('A', np.float64, (3,)),
        ('B', np.float64, (3,)),
        ('C', np.float64, (3,)),
        ('DOMAIN_ID', np.int64)
    ])

    Format = tables.descr_from_dtype(dtype)[0]

    @classmethod
    def _write_data(cls, h5f, cards, h5table):
        table_row = h5table.row

        domain = cls.domain_count

        ids = sorted(cards.keys())

        for _id in ids:
            data = cards[_id]

            def _get_val(val, default):
                return default if val in (None, '') else val

            table_row['CID'] = data[1]
            table_row['RID'] = _get_val(data[2], 0)
            table_row['A'] = data[3:6]
            table_row['B'] = data[6:9]
            table_row['C'] = data[9:12]
            table_row['DOMAIN_ID'] = domain

            table_row.append()

        h5f.flush()

    @classmethod
    def copy(cls):
        class _COPY(cls):
            pass

        return _COPY


class Cord2(CordCard):
    table_reader = Cord2Table
    dtype = Cord2Table.dtype


