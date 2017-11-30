from __future__ import print_function, absolute_import
from six import iteritems, itervalues
from six.moves import range

from tables import IsDescription, Int64Col, Float64Col, StringCol
import tables

from .._abstract_table import AbstractTable
from ._rigid_element import RigidElementCard

import numpy as np


class Rbe2Table(AbstractTable):
    group = '/NASTRAN/INPUT/RIGID_ELEMENT'
    table_id = 'RBE2'
    table_path = '%s/%s' % (group, table_id)
    identity_path = '%s/IDENTITY' % table_path
    data_path = '%s/DATA' % table_path

    dtype = np.dtype([
        ('RID', np.int64),
        ('GN', np.int64),
        ('CM', np.int64),
        ('ALPHA',np.float64),
        ('DATA_LEN', np.int64),
        ('DATA_POS', np.int64),
        ('DOMAIN_ID', np.int64)
    ])

    Format = tables.descr_from_dtype(dtype)[0]

    dtype_data = np.dtype([
        ('GM', np.int64),
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
            """:type data: pyNastran.bdf.cards.elements.rigid.RBE2"""

            identity_row['RID'] = data.eid
            identity_row['GN'] = data.gn
            identity_row['CM'] = data.cm
            identity_row['ALPHA'] = data.alpha

            identity_row['DATA_LEN'] = len(data.Gmi)
            identity_row['DATA_POS'] = data_pos
            identity_row['DOMAIN_ID'] = domain
            identity_row.append()

            data_pos += len(data.Gmi)

            dim_arr = np.zeros(len(data.Gmi), dtype=cls.dtype_data)
            dim_arr['GM'] = data.Gmi

            dim_data.append(dim_arr)

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


class RBE2(RigidElementCard):
    table_reader = Rbe2Table
    dtype = table_reader.dtype
    dtype_data = table_reader.dtype_data
    _id = 'RID'

    def __init__(self, bdf_data):
        super(RBE2, self).__init__(bdf_data)
        self.nodes = np.zeros(0, dtype=self.dtype_data)

    def resize(self, new_size):
        self.data.resize(new_size[0])
        self.nodes.resize(new_size[1])

    def set_data(self, data):
        self.resize((data[0].size, data[1].size))
        np.copyto(self.data, data[0])
        np.copyto(self.nodes, data[1])

