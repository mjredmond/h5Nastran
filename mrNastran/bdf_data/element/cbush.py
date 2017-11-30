from __future__ import print_function, absolute_import
from six import iteritems, itervalues
from six.moves import range

from tables import IsDescription, Int64Col, Float64Col, StringCol
import tables

from .._abstract_table import AbstractTable
from ._element import ElementCard

import numpy as np


class CbushTable(AbstractTable):
    group = '/NASTRAN/INPUT/ELEMENT'
    table_id = 'CBUSH'
    table_path = '%s/%s' % (group, table_id)

    dtype = np.dtype([
        ('EID', np.int64),
        ('PID', np.int64),
        ('GRID', np.int64, (2,)),
        ('X', np.float64, (3,)),
        ('G0', np.int64),
        ('CID', np.int64),
        ('S', np.float64),
        ('OCID', np.int64),
        ('S1', np.float64),
        ('S2', np.float64),
        ('S3', np.float64),
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
            """:type data: pyNastran.bdf.cards.elements.bush.CBUSH"""

            table_row['EID'] = data.eid
            table_row['PID'] = data.pid
            table_row['GRID'] = data.node_ids

            if data.g0 is None:
                table_row['G0'] = -1
                table_row['X'] = data.x

            table_row['CID'] = data.cid
            table_row['S'] = data.s
            table_row['OCID'] = data.ocid
            table_row['S1'] = data.si[0]
            table_row['S2'] = data.si[1]
            table_row['S3'] = data.si[2]

            table_row['DOMAIN_ID'] = domain

            table_row.append()

        h5f.flush()


class CBUSH(ElementCard):
    table_reader = CbushTable
    dtype = table_reader.dtype
