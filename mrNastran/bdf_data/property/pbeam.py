"""
"""
from __future__ import print_function, absolute_import
from six import iteritems, itervalues
from six.moves import range

from tables import IsDescription, Int64Col, Float64Col, StringCol
import tables

from .._abstract_table import AbstractTable
from .._cards import register_card
from ._property import PropertyCard

import numpy as np


class PbeamTable(AbstractTable):
    group = '/NASTRAN/INPUT/PROPERTY'
    table_id = 'PBEAM'
    table_path = '%s/%s' % (group, table_id)
    identity_path = '%s/IDENTITY' % table_path
    stress_recovery_path = '%s/STRESS_RECOVERY' % table_path

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
        ('STRESS_RECOVERY_LEN', np.int64),
        ('STRESS_RECOVERY_POS', np.int64),
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

            h5f.create_table(cls.table_path, 'STRESS_RECOVERY', cls.FormatSr, 'STRESS_RECOVERY',
                                    expectedrows=expected_rows, createparents=True)

            return h5f.get_node(cls.table_path)

    @classmethod
    def _write_data(cls, h5f, table_data, h5table):

        identity_row = h5table.IDENTITY.row
        stress_recovery = h5table.STRESS_RECOVERY

        domain = cls.domain_count

        ids = sorted(map(int, table_data.keys()))

        stress_recovery_pos = 0

        _sr_data = np.zeros(1, dtype=cls.dtype_sr)
        sr_data = _sr_data[0]

        comp = ['K1', 'K2', 'S1', 'S2', 'NSIA', 'NSIB', 'CWA', 'CWB', 'M1A', 'M2A',
                'M1B', 'M2B', 'N1A', 'N2A', 'N1B', 'N2B']

        comp_sr = ['SO', 'X_XB', 'A', 'I1', 'I2', 'I12', 'J', 'NSM', 'C1', 'C2', 'D1', 'D2',
                'E1', 'E2', 'F1', 'F2']

        # print(ids)

        for _id in ids:

            _id = str(_id)

            # TODO: what to do about multiple definitions?
            data_i = table_data[_id][0].data
            data_i_get = data_i.get

            # print(data_i)

            identity_row['PID'] = data_i[1]
            identity_row['MID'] = data_i_get(2, -1)

            sr_data['A'] = data_i_get(3, 0.)
            sr_data['I1'] = data_i_get(4, 0.)
            sr_data['I2'] = data_i_get(5, 0.)
            sr_data['I12'] = data_i_get(6, 0.)
            sr_data['J'] = data_i_get(7, 0.)
            sr_data['NSM'] = data_i_get(8, 0.)

            next_data = data_i_get(9, None)

            if isinstance(next_data, float) or next_data is None:
                sr_data['SO'] = b'YES'
                sr_data['X_XB'] = 0.
                sr_data['C1'] = next_data
                sr_data['C2'] = data_i_get(10, 0.)
                sr_data['D1'] = data_i_get(11, 0.)
                sr_data['D2'] = data_i_get(12, 0.)
                sr_data['E1'] = data_i_get(13, 0.)
                sr_data['E2'] = data_i_get(14, 0.)
                sr_data['F1'] = data_i_get(15, 0.)
                sr_data['F2'] = data_i_get(16, 0.)
                next_i = 17
            else:
                sr_data['SO'] = b'NO'
                sr_data['X_XB'] = 0.
                sr_data['C1'] = 0.
                sr_data['C2'] = 0.
                sr_data['D1'] = 0.
                sr_data['D2'] = 0.
                sr_data['E1'] = 0.
                sr_data['E2'] = 0.
                sr_data['F1'] = 0.
                sr_data['F2'] = 0.
                next_i = 9

            stress_recovery_data = [sr_data.tolist()]

            last_i = len(data_i) - 1

            sr_indices = []

            i = next_i

            while True:
                first_data = data_i_get(i, None)

                if isinstance(first_data, float):
                    break

                if first_data in ('YES', None):
                    sr_indices.append((i, 16))
                    i += 16
                else:
                    sr_indices.append((i, 8))
                    i += 8

                if i > last_i:
                    break

            for indices in sr_indices:
                i1 = indices[0]
                data_len = indices[1]

                _sr_data = np.zeros(1, dtype=cls.dtype_sr)
                sr_data = _sr_data[0]

                # print(i1)

                sr_data['SO'] = data_i[i1].encode()

                _i = 1
                for j in range(i1 + 1, i1 + data_len):
                    sr_data[comp_sr[_i]] = data_i_get(j, 0.)
                    _i += 1

                stress_recovery_data.append(sr_data.tolist())

            i_ = 0
            for i in range(i, i + 16):
                _comp = comp[i_]
                i_ += 1
                identity_row[_comp] = data_i_get(i, 0.)

            identity_row['STRESS_RECOVERY_LEN'] = len(stress_recovery_data)
            identity_row['STRESS_RECOVERY_POS'] = stress_recovery_pos

            identity_row['DOMAIN_ID'] = domain
            identity_row.append()

            stress_recovery_pos += len(stress_recovery_data)

            for i in range(len(stress_recovery_data)):
                stress_recovery.append([stress_recovery_data[i]])

        h5f.flush()

    @classmethod
    def read(cls, h5f):
        try:
            group = h5f.get_node(cls.table_path)
        except tables.NoSuchNodeError:
            return None, None

        identity = group.IDENTITY
        stress_recovery = group.STRESS_RECOVERY

        return identity.read(), stress_recovery.read()


@register_card
class PBEAM(PropertyCard):
    table_reader = PbeamTable
    dtype = table_reader.dtype
    dtype_sr = table_reader.dtype_sr

    def __init__(self, bdf_data):
        super(PBEAM, self).__init__(bdf_data)

        self.stress_recovery = np.zeros(0, dtype=self.dtype_sr)

    def resize(self, new_size):
        self._current_index = -1
        self._current_data = None

        self.data.resize(new_size[0])
        self.stress_recovery.resize(new_size[1])

    def set_data(self, data):
        self.resize((data[0].size, data[1].size))

        np.copyto(self.data, data[0])
        np.copyto(self.stress_recovery, data[1])

        self.update()

    def set_pid(self, pid):
        try:
            self._current_index = self.index[pid]
        except KeyError:
            raise ValueError('Unknown PID! %d' % pid)

        try:
            current_data = self.data[self._current_index]
        except IndexError:
            raise ValueError('PID %d not found in data!' % pid)

        i1 = current_data['STRESS_RECOVERY_POS']
        i2 = i1 + current_data['STRESS_RECOVERY_LEN']

        try:
            stress_recovery_data = self.stress_recovery[i1:i2]
        except IndexError:
            raise ValueError('PID %d has incorrect stress recovery indices!' % pid)

        self._current_data = (current_data, stress_recovery_data)
