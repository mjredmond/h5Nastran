from __future__ import print_function, absolute_import
from six import iteritems, itervalues
from six.moves import range

from tables import IsDescription, Int64Col, Float64Col, StringCol
import tables

from .._abstract_table import AbstractTable
from ._element import ElementCard

import numpy as np


class CbeamTable(AbstractTable):
    group = '/NASTRAN/INPUT/ELEMENT'
    table_id = 'CBEAM'
    table_path = '%s/%s' % (group, table_id)

    dtype = np.dtype([
        ('EID', np.int64),
        ('PID', np.int64),
        ('GRID', np.int64, (2,)),
        ('X', np.float64, (3,)),
        ('G0', np.int64),
        ('OFFT', 'S3'),
        ('BIT', np.float64),
        ('PA', np.int64),
        ('PB', np.int64),
        ('WA', np.float64, (3,)),
        ('WB', np.float64, (3,)),
        ('SA', np.int64),
        ('SB', np.int64),
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
            """:type data: pyNastran.bdf.cards.elements.beam.CBEAM"""

            table_row['EID'] = data.eid
            table_row['PID'] = data.pid
            table_row['GRID'] = data.node_ids

            if data.g0 is None:
                table_row['X'] = data.x
                table_row['G0'] = -1
            else:
                table_row['G0'] = data.g0
                table_row['X'] = 0.

            table_row['BIT'] = data.bit
            table_row['OFFT'] = data.offt

            table_row['PA'] = data.pa
            table_row['PB'] = data.pb

            table_row['WA'] = data.wa
            table_row['WB'] = data.wb

            table_row['SA'] = data.sa
            table_row['SB'] = data.sb

            table_row['DOMAIN_ID'] = domain

            table_row.append()

        h5f.flush()


class CBEAM(ElementCard):
    table_reader = CbeamTable
    dtype = table_reader.dtype
