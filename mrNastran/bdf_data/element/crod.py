from __future__ import print_function, absolute_import
from six import iteritems, itervalues
from six.moves import range

from tables import IsDescription, Int64Col, Float64Col, StringCol
import tables

from .._abstract_table import AbstractTable
from ._element import ElementCard

import numpy as np


class CrodTable(AbstractTable):
    group = '/NASTRAN/INPUT/ELEMENT'
    table_id = 'CROD'
    table_path = '%s/%s' % (group, table_id)

    dtype = np.dtype([
        ('EID', np.int64),
        ('PID', np.int64),
        ('GRID', np.int64, (2,)),
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
            """:type data: pyNastran.bdf.cards.elements.rods.CROD"""

            table_row['EID'] = data.eid
            table_row['PID'] = data.pid
            table_row['GRID'] = data.node_ids

            table_row['DOMAIN_ID'] = domain

            table_row.append()

        h5f.flush()


class CROD(ElementCard):
    table_reader = CrodTable
    dtype = table_reader.dtype
