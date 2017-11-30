from __future__ import print_function, absolute_import
from six import iteritems, itervalues
from six.moves import range

from tables import IsDescription, Int64Col, Float64Col, StringCol
import tables

from .._abstract_table import AbstractTable
from ._constraint import ConstraintCard

import numpy as np


class Spc1Table(AbstractTable):
    group = '/NASTRAN/INPUT/CONSTRAINT'
    table_id = 'SPC1'
    table_path = '%s/%s' % (group, table_id)

    dtype = np.dtype([
        ('SID', np.int64),
        ('C', np.int64),
        ('G', np.int64),
        ('DOMAIN_ID', np.int64)
    ])

    Format = tables.descr_from_dtype(dtype)[0]

    @classmethod
    def _write_data(cls, h5f, cards, h5table):
        table_row = h5table.row

        domain = cls.domain_count

        ids = sorted(cards.keys())

        for _id in ids:
            data_list = cards[_id]
            """:type data_list: list[pyNastran.bdf.cards.constraints.SPC1]"""

            for data in data_list:
                table_row['SID'] = data.conid
                table_row['C'] = data.components
                table_row['DOMAIN_ID'] = domain

                for nid in data.node_ids:
                    if nid is None:
                        continue
                    table_row['G'] = nid
                    table_row.append()

        h5f.flush()


class SPC1(ConstraintCard):
    table_reader = Spc1Table
    dtype = table_reader.dtype
