from __future__ import print_function, absolute_import
from six import iteritems, itervalues
from six.moves import range

from tables import IsDescription, Int64Col, Float64Col, StringCol
import tables

from .._abstract_table import AbstractTable
from ._property import PropertyCard

import numpy as np


class PcompTable(AbstractTable):
    group = '/NASTRAN/INPUT/PROPERTY'
    table_id = 'PCOMP'
    table_path = '%s/%s' % (group, table_id)
    identity_path = '%s/IDENTITY' % table_path
    data_path = '%s/DATA' % table_path

    dtype = np.dtype([
        ('PID', np.int64),
        ('Z0', np.float),
        ('NSM', np.float64),
        ('SB', np.float64),
        ('FT', 'S4'),
        ('TREF', np.float64),
        ('GE', np.float64),
        ('LAM', 'S6'),
        ('PLIES_LEN', np.int64),
        ('PLIES_LOC', np.int64),
        ('DOMAIN_ID', np.int64)
    ])

    Format = tables.descr_from_dtype(dtype)[0]

    dtype_data = np.dtype([
        ('MID', np.int64),
        ('T', np.float64),
        ('THETA', np.float64),
        ('SOUT', 'S3'),
    ])

    FormatPlies = tables.descr_from_dtype(dtype_data)[0]

    @classmethod
    def get_data_table(cls, h5f, expected_rows=1000000):
        try:
            return h5f.get_node(cls.table_path)
        except tables.NoSuchNodeError:
            h5f.create_table(cls.table_path, 'IDENTITY', cls.Format, 'IDENTITY',
                                    expectedrows=expected_rows, createparents=True)

            h5f.create_table(cls.table_path, 'DATA', cls.FormatPlies, 'DATA',
                                    expectedrows=expected_rows, createparents=True)

            return h5f.get_node(cls.table_path)

    @classmethod
    def _write_data(cls, h5f, cards, h5table):

        identity_row = h5table.IDENTITY.row
        plies = h5table.DATA

        domain = cls.domain_count

        ids = sorted(cards.keys())

        plies_loc = 0

        def _get_val(val, default):
            if val in ('', None):
                return default
            else:
                return val

        for _id in ids:
            data = cards[_id]
            """:type data: pyNastran.bdf.cards.properties.shell.PCOMP"""

            identity_row['PID'] = data.pid
            identity_row['Z0'] = data.z0
            identity_row['NSM'] = data.nsm
            identity_row['SB'] = data.sb
            identity_row['FT'] = _get_val(data.ft, '')
            identity_row['TREF'] = data.tref
            identity_row['GE'] = data.ge
            identity_row['LAM'] = _get_val(data.lam, '')
            identity_row['PLIES_LOC'] = plies_loc

            _plies = data.plies
            plies.append(_plies)

            identity_row['PLIES_LEN'] = len(_plies)
            identity_row['DOMAIN_ID'] = domain
            identity_row.append()

            plies_loc += len(_plies)

        h5f.flush()

    @classmethod
    def read(cls, h5f):
        try:
            group = h5f.get_node(cls.table_path)
        except tables.NoSuchNodeError:
            return None, None

        identity = group.IDENTITY
        plies = group.DATA

        return identity.read(), plies.read()


class PCOMP(PropertyCard):
    table_reader = PcompTable
    dtype = table_reader.dtype
    dtype_data = table_reader.dtype_data

    def __init__(self, bdf_data):
        super(PCOMP, self).__init__(bdf_data)
        self.plies = np.zeros(0, dtype=self.dtype_data)

    def resize(self, new_size):
        self.data.resize(new_size[0])
        self.plies.resize(new_size[1])

    def set_data(self, data):
        self.resize((data[0].size, data[1].size))
        np.copyto(self.data, data[0])
        np.copyto(self.plies, data[1])

