from __future__ import print_function, absolute_import
from six import iteritems, iterkeys, itervalues
from six.moves import range

import numpy as np
import tables

from .._abstract_table import AbstractTable
from ._node import NodeCard


class GridTable(AbstractTable):
    group = '/NASTRAN/INPUT/NODE'
    table_id = 'GRID'
    table_path = '%s/%s' % (group, table_id)

    dtype = np.dtype([
        ('ID', np.int64),
        ('CP', np.int64),
        ('X', np.float64, (3,)),
        ('CD', np.int64),
        ('PS', np.int64),
        ('SEID', np.int64),
        ('DOMAIN_ID', np.int64)
    ])

    Format = tables.descr_from_dtype(dtype)[0]

    @classmethod
    def _write_data(cls, h5f, cards, h5table):
        table_row = h5table.row

        domain = cls.domain_count

        ids = sorted(cards.keys())

        def _get_val(val):
            if val == '':
                return -1
            return int(val)

        for _id in ids:
            data = cards[_id]
            """:type data: pyNastran.bdf.cards.nodes.GRID"""

            table_row['ID'] = data.nid
            table_row['CP'] = data.cp
            table_row['X'] = data.xyz
            table_row['CD'] = data.cd
            table_row['PS'] = _get_val(data.ps)
            table_row['SEID'] = data.seid
            table_row['DOMAIN_ID'] = domain

            table_row.append()

        h5f.flush()


class GRID(NodeCard):
    table_reader = GridTable
    dtype = GridTable.dtype
