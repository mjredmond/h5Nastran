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
            """:type data: pyNastran.bdf.cards.coordinate_systems.Cord2x"""

            table_row['CID'] = data.cid
            table_row['RID'] = data.rid
            table_row['A'] = data.e1
            table_row['B'] = data.e2
            table_row['C'] = data.e3
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


