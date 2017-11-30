from __future__ import print_function, absolute_import
from six import iteritems, itervalues
from six.moves import range

from tables import IsDescription, Int64Col, Float64Col, StringCol
import tables

from .._abstract_table import AbstractTable
from ._property import PropertyCard

import numpy as np


class PshellTable(AbstractTable):
    group = '/NASTRAN/INPUT/PROPERTY'
    table_id = 'PSHELL'
    table_path = '%s/%s' % (group, table_id)

    dtype = np.dtype([
        ('PID', np.int64),
        ('MID1', np.int64),
        ('T', np.float64),
        ('MID2', np.int64),
        ('I', np.float64),
        ('MID3', np.int64),
        ('TST', np.float64),
        ('NSM', np.float64),
        ('Z1', np.float64),
        ('Z2', np.float64),
        ('MID4', np.int64),
        ('DOMAIN_ID', np.int64)
    ])

    Format = tables.descr_from_dtype(dtype)[0]

    @classmethod
    def _write_data(cls, h5f, cards, h5table):
        table_row = h5table.row

        domain = cls.domain_count

        ids = sorted(cards.keys())

        def _get_val(val, default):
            if val in ('', None):
                return default
            else:
                return val

        for _id in ids:
            data = cards[_id]
            """:type data: pyNastran.bdf.cards.properties.shell.PSHELL"""

            table_row['PID'] = data.pid
            table_row['MID1'] = data.mid1
            table_row['T'] = data.t
            table_row['MID2'] = _get_val(data.mid2, -1)
            table_row['I'] = _get_val(data.twelveIt3, np.nan)
            table_row['MID3'] = _get_val(data.mid3, -1)
            table_row['TST'] = _get_val(data.tst, np.nan)
            table_row['NSM'] = _get_val(data.nsm, np.nan)
            table_row['Z1'] = _get_val(data.z1, np.nan)
            table_row['Z2'] = _get_val(data.z2, np.nan)
            table_row['MID4'] = _get_val(data.mid4, -1)

            table_row['DOMAIN_ID'] = domain

            table_row.append()

        h5f.flush()


class PSHELL(PropertyCard):
    table_reader = PshellTable
    dtype = table_reader.dtype
