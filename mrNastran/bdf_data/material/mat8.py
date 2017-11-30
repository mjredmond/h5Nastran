from __future__ import print_function, absolute_import
from six import iteritems, itervalues
from six.moves import range

from tables import IsDescription, Int64Col, Float64Col, StringCol
import tables

from .._abstract_table import AbstractTable
from ._material import MaterialCard

import numpy as np


class Mat8Table(AbstractTable):
    group = '/NASTRAN/INPUT/MATERIAL'
    table_id = 'MAT8'
    table_path = '%s/%s' % (group, table_id)

    dtype = np.dtype([
        ('MID', np.int64),
        ('E1', np.float64),
        ('E2', np.float64),
        ('NU12', np.float64),
        ('G12', np.float64),
        ('G1Z', np.float64),
        ('G2Z', np.float64),
        ('RHO', np.float64),
        ('A1', np.float64),
        ('A2', np.float64),
        ('TREF', np.float64),
        ('XT', np.float64),
        ('XC', np.float64),
        ('YT', np.float64),
        ('YC', np.float64),
        ('S', np.float64),
        ('GE', np.float64),
        ('F12', np.float64),
        ('STRN', np.float64),
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
            """:type data: pyNastran.bdf.cards.materials.MAT8"""

            table_row['MID'] = data.mid
            table_row['E1'] = data.e11
            table_row['E2'] = data.e22
            table_row['NU12'] = data.nu12
            table_row['G12'] = data.g12
            table_row['G1Z'] = data.g1z
            table_row['G2Z'] = data.g2z
            table_row['RHO'] = data.rho
            table_row['A1'] = data.a1
            table_row['A2'] = data.a2
            table_row['TREF'] = data.tref
            table_row['XT'] = data.Xt
            table_row['XC'] = data.Xc
            table_row['YT'] = data.Yt
            table_row['YC'] = data.Yc
            table_row['S'] = data.S
            table_row['GE'] = data.ge
            table_row['F12'] = data.F12
            table_row['STRN'] = data.strn

            table_row['DOMAIN_ID'] = domain

            table_row.append()

        h5f.flush()


class MAT8(MaterialCard):
    table_reader = Mat8Table
    dtype = table_reader.dtype
