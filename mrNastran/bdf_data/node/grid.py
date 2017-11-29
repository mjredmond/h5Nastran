from __future__ import print_function, absolute_import
from six import iteritems, iterkeys, itervalues
from six.moves import range

import numpy as np
import tables

from .._abstract_table import AbstractTable
from .._abstract_card import AbstractCard


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

        for _id in ids:
            data = cards[_id]

            def _get_val(data_):
                return 0 if data_ in (None, '') else data_

            table_row['ID'] = data[1]
            table_row['CP'] = _get_val(data[2])
            table_row['X'] = data[3], data[4], data[5]
            table_row['CD'] = _get_val(data[6])
            table_row['PS'] = _get_val(data[7])
            table_row['SEID'] = _get_val(data[8])
            table_row['DOMAIN_ID'] = domain

            table_row.append()

        h5f.flush()


class GRID(AbstractCard):
    card_type = 'GRID'
    table_reader = GridTable
    dtype = GridTable.dtype
    _id = 'ID'
