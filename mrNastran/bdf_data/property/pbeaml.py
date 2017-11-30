from __future__ import print_function, absolute_import
from six import iteritems, itervalues
from six.moves import range

from tables import IsDescription, Int64Col, Float64Col, StringCol
import tables

from .._abstract_table import AbstractTable
from ._property import PropertyCard

import numpy as np


class PbeamlTable(AbstractTable):
    group = '/NASTRAN/INPUT/PROPERTY'
    table_id = 'PBEAML'
    table_path = '%s/%s' % (group, table_id)
    identity_path = '%s/IDENTITY' % table_path
    data_path = '%s/DATA' % table_path

    dtype = np.dtype([
        ('PID', np.int64),
        ('MID', np.int64),
        ('GROUP', 'S16'),
        ('TYPE', 'S8'),
        ('DATA_LEN', np.int64),
        ('DATA_POS', np.int64),
        ('DOMAIN_ID', np.int64)
    ])

    Format = tables.descr_from_dtype(dtype)[0]

    dtype_data = np.dtype([
        ('DIM', np.float64, (12,)),
        ('NSM', np.float64),
        ('SO', 'S3'),
        ('X_XB', np.float64)
    ])

    FormatData = tables.descr_from_dtype(dtype_data)[0]

    @classmethod
    def get_data_table(cls, h5f, expected_rows=1000000):
        try:
            return h5f.get_node(cls.table_path)
        except tables.NoSuchNodeError:
            h5f.create_table(cls.table_path, 'IDENTITY', cls.Format, 'IDENTITY',
                                    expectedrows=expected_rows, createparents=True)

            h5f.create_table(cls.table_path, 'DATA', cls.FormatData, 'DATA',
                             expectedrows=expected_rows, createparents=True)

            return h5f.get_node(cls.table_path)

    @classmethod
    def _write_data(cls, h5f, cards, h5table):

        identity_row = h5table.IDENTITY.row
        dim_data = h5table.DATA

        domain = cls.domain_count

        ids = sorted(cards.keys())

        data_pos = 0

        for _id in ids:
            data = cards[_id]
            """:type data: pyNastran.bdf.cards.properties.beam.PBEAML"""

            identity_row['PID'] = data.pid
            identity_row['MID'] = data.mid
            identity_row['GROUP'] = data.group
            identity_row['TYPE'] = data.beam_type

            xcount = len(data.so)

            identity_row['DATA_LEN'] = xcount
            identity_row['DATA_POS'] = data_pos
            identity_row['DOMAIN_ID'] = domain
            identity_row.append()

            data_pos += xcount

            _dim_data = np.zeros(xcount, dtype=cls.dtype_data)

            _dims = []
            for _dim in data.dim:
                if len(_dim) < 12:
                    _dim.extend([np.nan] * (12 - len(_dim)))
                _dims.append(_dim)

            _dim_data['DIM'] = _dims
            _dim_data['NSM'] = data.nsm
            _dim_data['SO'] = data.so
            _dim_data['X_XB'] = data.xxb

            dim_data.append(_dim_data)

        h5f.flush()

    @classmethod
    def read(cls, h5f):
        try:
            group = h5f.get_node(cls.table_path)
        except tables.NoSuchNodeError:
            return None, None

        identity = group.IDENTITY
        dims = group.DATA

        return identity.read(), dims.read()


class PBEAML(PropertyCard):
    table_reader = PbeamlTable
    dtype = table_reader.dtype
    dtype_data = table_reader.dtype_data

    def __init__(self, bdf_data):
        super(PBEAML, self).__init__(bdf_data)
        self.dims = np.zeros(0, dtype=self.dtype_data)

    def resize(self, new_size):
        self.data.resize(new_size[0])
        self.dims.resize(new_size[1])

    def set_data(self, data):
        self.resize((data[0].size, data[1].size))
        np.copyto(self.data, data[0])
        np.copyto(self.dims, data[1])

