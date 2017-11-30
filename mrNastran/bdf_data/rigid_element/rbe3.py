from __future__ import print_function, absolute_import
from six import iteritems, itervalues
from six.moves import range

from tables import IsDescription, Int64Col, Float64Col, StringCol
import tables

from .._abstract_table import AbstractTable
from ._rigid_element import RigidElementCard

import numpy as np


class Rbe3Table(AbstractTable):
    group = '/NASTRAN/INPUT/RIGID_ELEMENT'
    table_id = 'RBE3'
    table_path = '%s/%s' % (group, table_id)
    identity_path = '%s/IDENTITY' % table_path
    data_path = '%s/DATA' % table_path

    dtype = np.dtype([
        ('RID', np.int64),
        ('REFGRID', np.int64),
        ('REFC', np.int64),
        ('ALPHA',np.float64),
        ('INDEPENDENT_LEN', np.int64),
        ('INDEPENDENT_POS', np.int64),
        ('DEPENDENT_LEN', np.int64),
        ('DEPENDENT_POS', np.int64),
        ('DOMAIN_ID', np.int64)
    ])

    Format = tables.descr_from_dtype(dtype)[0]

    dtype_independent = np.dtype([
        ('WT', np.float64),
        ('C', np.int64),
        ('G', np.int64),
    ])

    FormatIndependent = tables.descr_from_dtype(dtype_independent)[0]

    dtype_dependent = np.dtype([
        ('GM', np.int64),
        ('CM', np.int64)
    ])

    FormatDependent = tables.descr_from_dtype(dtype_dependent)[0]

    @classmethod
    def get_data_table(cls, h5f, expected_rows=1000000):
        try:
            return h5f.get_node(cls.table_path)
        except tables.NoSuchNodeError:
            h5f.create_table(cls.table_path, 'IDENTITY', cls.Format, 'IDENTITY',
                                    expectedrows=expected_rows, createparents=True)

            h5f.create_table(cls.table_path, 'INDEPENDENT', cls.FormatIndependent, 'INDEPENDENT',
                             expectedrows=expected_rows, createparents=True)

            h5f.create_table(cls.table_path, 'DEPENDENT', cls.FormatDependent, 'DEPENDENT',
                             expectedrows=expected_rows, createparents=True)

            return h5f.get_node(cls.table_path)

    @classmethod
    def _write_data(cls, h5f, cards, h5table):

        identity_row = h5table.IDENTITY.row
        independent_row = h5table.INDEPENDENT.row
        dependent_row = h5table.DEPENDENT.row

        domain = cls.domain_count

        ids = sorted(cards.keys())

        independent_pos = 0
        dependent_pos = 0

        for _id in ids:
            data = cards[_id]
            """:type data: pyNastran.bdf.cards.elements.rigid.RBE3"""

            identity_row['RID'] = data.eid
            identity_row['REFGRID'] = data.refgrid
            identity_row['REFC'] = data.refc
            identity_row['ALPHA'] = data.alpha

            independent_length = len(data.weights)
            dependent_length = len(data.Gmi)

            identity_row['INDEPENDENT_LEN'] = independent_length
            identity_row['INDEPENDENT_POS'] = independent_pos

            identity_row['DEPENDENT_LEN'] = dependent_length
            identity_row['DEPENDENT_POS'] = dependent_pos

            independent_pos += independent_length
            dependent_pos += dependent_length

            identity_row['DOMAIN_ID'] = domain
            identity_row.append()

            for i in range(independent_length):
                grids = data.Gijs[i]
                for grid in grids:
                    independent_row['WT'] = data.weights[i]
                    independent_row['C'] = data.comps[i]
                    independent_row['G'] = grid
                    independent_row.append()

            for i in range(dependent_length):
                dependent_row['GM'] = data.Gmi[i]
                dependent_row.append()

        h5f.flush()

    @classmethod
    def read(cls, h5f):
        try:
            group = h5f.get_node(cls.table_path)
        except tables.NoSuchNodeError:
            return None, None

        identity = group.IDENTITY
        independent = group.INDEPENDENT
        dependent = group.DEPENDENT

        return identity.read(), independent.read(), dependent.read()


class RBE3(RigidElementCard):
    table_reader = Rbe3Table
    dtype = table_reader.dtype
    dtype_independent = table_reader.dtype_independent
    dtype_dependent = table_reader.dtype_dependent

    def __init__(self, bdf_data):
        super(RBE3, self).__init__(bdf_data)
        self.independent = np.zeros(0, dtype=self.dtype_independent)
        self.dependent = np.zeros(0, dtype=self.dtype_dependent)

    def resize(self, new_size):
        self.data.resize(new_size[0])
        self.independent.resize(new_size[1])
        self.dependent.resize(new_size[2])

    def set_data(self, data):
        self.resize((data[0].size, data[1].size, data[2].size))
        np.copyto(self.data, data[0])
        np.copyto(self.independent, data[1])
        np.copyto(self.dependent, data[2])
