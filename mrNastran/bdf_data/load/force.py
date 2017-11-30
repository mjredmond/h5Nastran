from __future__ import print_function, absolute_import
from six import iteritems, itervalues
from six.moves import range

from tables import IsDescription, Int64Col, Float64Col, StringCol
import tables

from .._abstract_table import AbstractTable
from ._load import LoadCard

import numpy as np


class ForceTable(AbstractTable):
    group = '/NASTRAN/INPUT/LOAD'
    table_id = 'FORCE'
    table_path = '%s/%s' % (group, table_id)

    dtype = np.dtype([
        ('SID', np.int64),
        ('G', np.int64),
        ('CID', np.int64),
        ('F', np.float64),
        ('N', np.float64, (3,)),
        ('DOMAIN_ID', np.int64)
    ])

    Format = tables.descr_from_dtype(dtype)[0]

    @classmethod
    def _write_data(cls, h5f, cards, h5table):
        table_row = h5table.row

        domain = cls.domain_count

        eids = sorted(cards.keys())

        def _get_val(val, default):
            return default if val in (None, '') else val

        for eid in eids:
            data_list = cards[eid]
            """:type data_list: list[pyNastran.bdf.cards.loads.static_loads.FORCE]"""

            for data in data_list:
                table_row['SID'] = data.sid
                table_row['G'] = data.node
                table_row['CID'] = data.cid
                table_row['F'] = data.mag
                table_row['N'] = data.xyz

                table_row['DOMAIN_ID'] = domain

                table_row.append()

        h5f.flush()


class FORCE(LoadCard):
    table_reader = ForceTable
    dtype = table_reader.dtype
    _id = 'SID'
