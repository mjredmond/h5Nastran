from __future__ import print_function, absolute_import
from six import iteritems, itervalues
from six.moves import range

from tables import IsDescription, Int64Col, Float64Col, StringCol
import tables

from .._abstract_table import AbstractTable
from ._material import MaterialCard

import numpy as np


class Mat4Table(AbstractTable):
    group = '/NASTRAN/INPUT/MATERIAL'
    table_id = 'MAT4'
    table_path = '%s/%s' % (group, table_id)

    dtype = np.dtype([
        ('MID', np.int64),
        ('K', np.float64),
        ('CP', np.float64),
        ('RHO', np.float64),
        ('H', np.float64),
        ('MU', np.float64),
        ('HGEN', np.float64),
        ('REFENTH', np.float64),
        ('TCH', np.float64),
        ('TDELTA', np.float64),
        ('QLAT', np.float64),
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
            """:type data: pyNastran.bdf.cards.materials.MAT4"""

            table_row['MID'] = data.mid
            table_row['K'] = data.k
            table_row['CP'] = data.cp
            table_row['RHO'] = data.rho
            table_row['H'] = data.H
            table_row['MU'] = data.mu
            table_row['HGEN'] = data.hgen
            table_row['REFENTH'] = data.ref_enthalpy
            table_row['TCH'] = data.tch
            table_row['TDELTA'] = data.tdelta
            table_row['QLAT'] = data.qlat

            table_row['DOMAIN_ID'] = domain

            table_row.append()

        h5f.flush()


class MAT4(MaterialCard):
    table_reader = Mat4Table
    dtype = table_reader.dtype
