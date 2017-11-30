from __future__ import print_function, absolute_import
from six import iteritems, itervalues
from six.moves import range

from tables import IsDescription, Int64Col, Float64Col, StringCol
import tables

from .._abstract_table import AbstractTable
from ._property import PropertyCard

import numpy as np


class PbushTable(AbstractTable):
    group = '/NASTRAN/INPUT/PROPERTY'
    table_id = 'PBUSH'
    table_path = '%s/%s' % (group, table_id)

    dtype = np.dtype([
        ('PID', np.int64),
        ('K', np.float64, (6,)),
        ('B', np.float64, (6,)),
        ('GE', np.float64, (6,)),
        ('SA', np.float64),
        ('ST', np.float64),
        ('EA', np.float64),
        ('ET', np.float64),
        ('DOMAIN_ID', np.int64)
    ])

    Format = tables.descr_from_dtype(dtype)[0]

    @classmethod
    def _write_data(cls, h5f, cards, h5table):
        table_row = h5table.row

        domain = cls.domain_count

        ids = sorted(cards.keys())

        def _get_val(obj, attr):
            try:
                return getattr(obj, attr)
            except AttributeError:
                return np.nan

        for _id in ids:
            data = cards[_id]
            """:type data: pyNastran.bdf.cards.properties.bush.PBUSH"""

            table_row['PID'] = data.pid

            if len(data.Ki) == 0:
                table_row['K'] = 0.
            else:
                table_row['K'] = data.Ki

            if len(data.Bi) == 0:
                table_row['B'] = 0.
            else:
                table_row['B'] = data.Bi

            if len(data.GEi) == 0:
                table_row['GE'] = 0.
            else:
                table_row['GE'] = data.GEi

            # FIXME: pynastran should always have the attributes below defined, even if None
            table_row['SA'] = _get_val(data, 'sa')
            table_row['ST'] = _get_val(data, 'st')
            table_row['EA'] = _get_val(data, 'ea')
            table_row['ET'] = _get_val(data, 'et')

            table_row['DOMAIN_ID'] = domain

            table_row.append()

        h5f.flush()


class PBUSH(PropertyCard):
    table_reader = PbushTable
    dtype = table_reader.dtype
