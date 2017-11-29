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

            def _get_val(val, default):
                return default if val in (None, '') else val

            table_row['EID'] = data[1]
            table_row['PID'] = _get_val(data[2], data[1])
            table_row['GRID'] = data[3:5]

            tmp = data[5:8]

            if tmp.count(None) == 3:
                table_row['G0'] = data[3]
                table_row['X'] = 0.
            elif isinstance(data[5], int):
                table_row['G0'] = data[5]
            else:
                table_row['G0'] = -1
                table_row['X'] = data[5:8]

            offt_bit = _get_val(data[8], 0.)

            if isinstance(offt_bit, float):
                table_row['BIT'] = offt_bit
                table_row['OFFT'] = ''
            else:
                table_row['OFFT'] = offt_bit
                table_row['BIT'] = np.nan

            table_row['PA'] = _get_val(data[9], 0)
            table_row['PB'] = _get_val(data[10], 0)

            wa = (_get_val(data[11], 0.), _get_val(data[12], 0.), _get_val(data[13], 0.))
            wb = (_get_val(data[14], 0.), _get_val(data[15], 0.), _get_val(data[16], 0.))

            table_row['WA'] = wa
            table_row['WB'] = wb

            table_row['SA'] = _get_val(data[17], 0)
            table_row['SB'] = _get_val(data[18], 0)

            table_row['DOMAIN_ID'] = domain

            table_row.append()

        h5f.flush()


class CBEAM(ElementCard):
    table_reader = CbeamTable
    dtype = table_reader.dtype
    _id = 'EID'
