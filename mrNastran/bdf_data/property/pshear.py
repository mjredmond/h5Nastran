from __future__ import print_function, absolute_import
from six import iteritems, itervalues
from six.moves import range

from tables import IsDescription, Int64Col, Float64Col, StringCol
import tables

from .._abstract_table import AbstractTable
from ._property import PropertyCard

import numpy as np


class PshearTable(AbstractTable):
    group = '/NASTRAN/INPUT/PROPERTY'
    table_id = 'PSHEAR'
    table_path = '%s/%s' % (group, table_id)

    dtype = np.dtype([
        ('PID', np.int64),
        ('MID', np.int64),
        ('T', np.float64),
        ('NSM', np.float64),
        ('F1', np.float64),
        ('F2', np.float64),
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
            """:type data: pyNastran.bdf.cards.properties.shell.PSHEAR"""

            table_row['PID'] = data.pid
            table_row['MID'] = data.mid
            table_row['T'] = data.t
            table_row['NSM'] = data.nsm
            table_row['F1'] = data.f1
            table_row['F2'] = data.f2

            table_row['DOMAIN_ID'] = domain

            table_row.append()

        h5f.flush()


class PSHEAR(PropertyCard):
    table_reader = PshearTable
    dtype = table_reader.dtype

