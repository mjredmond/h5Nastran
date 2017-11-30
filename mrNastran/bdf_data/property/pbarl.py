from __future__ import print_function, absolute_import
from six import iteritems, itervalues
from six.moves import range

from tables import IsDescription, Int64Col, Float64Col, StringCol
import tables

from .._abstract_table import AbstractTable
from ._property import PropertyCard

import numpy as np


class PbarlTable(AbstractTable):
    group = '/NASTRAN/INPUT/PROPERTY'
    table_id = 'PBARL'
    table_path = '%s/%s' % (group, table_id)
    identity_path = '%s/IDENTITY' % table_path
    data_path = '%s/DATA' % table_path

    dtype = np.dtype([
        ('PID', np.int64),
        ('MID', np.int64),
        ('GROUP', 'S16'),
        ('TYPE', 'S8'),
        ('NSM', np.float64),
        ('DIM', np.float64, (12,)),
        ('DOMAIN_ID', np.int64)
    ])

    Format = tables.descr_from_dtype(dtype)[0]

    @classmethod
    def get_data_table(cls, h5f, expected_rows=1000000):
        try:
            return h5f.get_node(cls.table_path)
        except tables.NoSuchNodeError:
            h5f.create_table(cls.group, cls.table_id, cls.Format, cls.table_id,
                                    expectedrows=expected_rows, createparents=True)

            return h5f.get_node(cls.table_path)

    @classmethod
    def _write_data(cls, h5f, cards, h5table):
        table_row = h5table.row

        domain = cls.domain_count

        ids = sorted(cards.keys())

        for _id in ids:
            data = cards[_id]
            """:type data: pyNastran.bdf.cards.properties.bars.PBARL"""

            table_row['PID'] = data.pid
            table_row['MID'] = data.mid
            table_row['GROUP'] = data.group
            table_row['TYPE'] = data.beam_type
            table_row['NSM'] = data.nsm

            dims = list(data.dim)

            if len(dims) < 12:
                dims.extend([np.nan] * (12 - len(dims)))

            table_row['DIM'] = dims

            table_row['DOMAIN_ID'] = domain
            table_row.append()

        h5f.flush()


class PBARL(PropertyCard):
    table_reader = PbarlTable
    dtype = table_reader.dtype

