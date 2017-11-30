from __future__ import print_function, absolute_import
from six import iteritems, itervalues
from six.moves import range

from tables import IsDescription, Int64Col, Float64Col, StringCol
import tables

from .._abstract_table import AbstractTable
from ._property import PropertyCard

import numpy as np


class PbeamTable(AbstractTable):
    group = '/NASTRAN/INPUT/PROPERTY'
    table_id = 'PBEAM'
    table_path = '%s/%s' % (group, table_id)
    identity_path = '%s/IDENTITY' % table_path
    data_path = '%s/DATA' % table_path

    dtype = np.dtype([
        ('PID', np.int64),
        ('MID', np.int64),
        ('K1', np.float64),
        ('K2', np.float64),
        ('S1', np.float64),
        ('S2', np.float64),
        ('NSIA', np.float64),
        ('NSIB', np.float64),
        ('CWA', np.float64),
        ('CWB', np.float64),
        ('M1A', np.float64),
        ('M2A', np.float64),
        ('M1B', np.float64),
        ('M2B', np.float64),
        ('N1A', np.float64),
        ('N2A', np.float64),
        ('N1B', np.float64),
        ('N2B', np.float64),
        ('DATA_LEN', np.int64),
        ('DATA_POS', np.int64),
        ('DOMAIN_ID', np.int64)
    ])

    Format = tables.descr_from_dtype(dtype)[0]

    dtype_sr = np.dtype([
        ('SO', 'S8'),
        ('X_XB', np.float64),
        ('A', np.float64),
        ('I1', np.float64),
        ('I2', np.float64),
        ('I12', np.float64),
        ('J', np.float64),
        ('NSM', np.float64),
        ('C1', np.float64),
        ('C2', np.float64),
        ('D1', np.float64),
        ('D2', np.float64),
        ('E1', np.float64),
        ('E2', np.float64),
        ('F1', np.float64),
        ('F2', np.float64)
    ])

    FormatSr = tables.descr_from_dtype(dtype_sr)[0]

    @classmethod
    def get_data_table(cls, h5f, expected_rows=1000000):
        try:
            return h5f.get_node(cls.table_path)
        except tables.NoSuchNodeError:
            h5f.create_table(cls.table_path, 'IDENTITY', cls.Format, 'IDENTITY',
                                    expectedrows=expected_rows, createparents=True)

            h5f.create_table(cls.table_path, 'DATA', cls.FormatSr, 'DATA',
                                    expectedrows=expected_rows, createparents=True)

            return h5f.get_node(cls.table_path)

    @classmethod
    def _write_data(cls, h5f, cards, h5table):

        identity_row = h5table.IDENTITY.row
        stress_recovery = h5table.DATA

        domain = cls.domain_count

        ids = sorted(cards.keys())

        stress_recovery_pos = 0

        names = cls.dtype.names

        for _id in ids:
            data = cards[_id]
            """:type data: pyNastran.bdf.cards.properties.beam.PBEAM"""

            for i in range(len(names)-3):
                name = str(names[i])
                identity_row[names[i]] = getattr(data, name.lower())

            sr_data = np.zeros(data.so.shape[0], dtype=cls.dtype_sr)
            sr_data['SO'] = data.so
            sr_data['X_XB'] = data.xxb
            sr_data['C1'] = data.c1
            sr_data['C2'] = data.c2
            sr_data['D1'] = data.d1
            sr_data['D2'] = data.d2
            sr_data['E1'] = data.e1
            sr_data['E2'] = data.e2
            sr_data['F1'] = data.f1
            sr_data['F2'] = data.f2

            identity_row['DATA_LEN'] = sr_data.shape[0]
            identity_row['DATA_POS'] = stress_recovery_pos

            identity_row['DOMAIN_ID'] = domain
            identity_row.append()

            stress_recovery_pos += sr_data.shape[0]
            stress_recovery.append(sr_data)

        h5f.flush()

    @classmethod
    def read(cls, h5f):
        try:
            group = h5f.get_node(cls.table_path)
        except tables.NoSuchNodeError:
            return None, None

        identity = group.IDENTITY
        stress_recovery = group.DATA

        return identity.read(), stress_recovery.read()


class PBEAM(PropertyCard):
    table_reader = PbeamTable
    dtype = table_reader.dtype
    dtype_sr = table_reader.dtype_sr

    def __init__(self, bdf_data):
        super(PBEAM, self).__init__(bdf_data)
        self.stress_recovery = np.zeros(0, dtype=self.dtype_sr)

    def resize(self, new_size):
        self.data.resize(new_size[0])
        self.stress_recovery.resize(new_size[1])

    def set_data(self, data):
        self.resize((data[0].size, data[1].size))
        np.copyto(self.data, data[0])
        np.copyto(self.stress_recovery, data[1])

