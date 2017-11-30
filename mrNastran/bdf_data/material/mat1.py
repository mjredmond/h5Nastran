from __future__ import print_function, absolute_import
from six import iteritems, itervalues
from six.moves import range

from tables import IsDescription, Int64Col, Float64Col, StringCol
import tables

from .._abstract_table import AbstractTable
from ._material import MaterialCard

import numpy as np


class Mat1Table(AbstractTable):
    group = '/NASTRAN/INPUT/MATERIAL'
    table_id = 'MAT1'
    table_path = '%s/%s' % (group, table_id)

    dtype = np.dtype([
        ('MID', np.int64),
        ('E', np.float64),
        ('G', np.float64),
        ('NU', np.float64),
        ('RHO', np.float64),
        ('A', np.float64),
        ('TREF', np.float64),
        ('GE', np.float64),
        ('ST', np.float64),
        ('SC', np.float64),
        ('SS', np.float64),
        ('MCSID', np.int64),
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
            """:type data: pyNastran.bdf.cards.materials.MAT1"""

            table_row['MID'] = data.mid
            table_row['E'] = data.e
            table_row['G'] = data.g
            table_row['NU'] = data.nu
            table_row['RHO'] = data.rho
            table_row['A'] = data.a
            table_row['TREF'] = data.tref
            table_row['GE'] = data.ge
            table_row['ST'] = data.St
            table_row['SC'] = data.Sc
            table_row['SS'] = data.Ss
            table_row['MCSID'] = data.mcsid

            table_row['DOMAIN_ID'] = domain

            table_row.append()

        h5f.flush()


class MAT1(MaterialCard):
    table_reader = Mat1Table
    dtype = table_reader.dtype
