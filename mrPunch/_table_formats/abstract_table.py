"""
"""
from __future__ import print_function, absolute_import
from six import iteritems, itervalues
from six.moves import range


import tables
import numpy as np

from .table_index import TableIndex


class AbstractTable(object):

    group = ''
    table_id = ''
    table_path = ''
    results_type = ''

    index_columns = []

    domain_count = 0

    class Format(object):
        def __init__(self):
            raise NotImplementedError

    class IndexFormat(tables.IsDescription):
        DOMAIN_ID = tables.Int64Col(pos=1)
        POSITION = tables.Int64Col(pos=2)
        LENGTH = tables.Int64Col(pos=3)

    @classmethod
    def write_data(cls, h5f, table_data):
        cls.domain_count += 1
        cls._write_data(h5f, table_data, cls.get_table(h5f))

    @classmethod
    def _write_data(cls, h5f, table_data, h5table):
        raise NotImplementedError

    @classmethod
    def get_table(cls, h5f, expected_rows=1000000):
        try:
            return h5f.get_node(cls.table_path)
        except tables.NoSuchNodeError:
            return h5f.create_table(cls.group, cls.table_id, cls.Format, cls.results_type,
                                    expectedrows=expected_rows, createparents=True)

    @classmethod
    def finalize(cls, h5f):
        cls._write_index(h5f)
        cls._write_private_index(h5f)

    @classmethod
    def _write_private_index(cls, h5f):
        table = cls.get_table(h5f)

        # noinspection PyProtectedMember
        col1 = table.cols._f_col(cls.index_columns[0])[:]

        try:
            # noinspection PyProtectedMember
            col2 = table.cols._f_col(cls.index_columns[1])[:]
        except IndexError:
            col2 = None

        if col2 is not None:
            data = np.empty((col1.size, 2), dtype=col1.dtype)
            data[:, 0] = col1
            data[:, 1] = col2
        else:
            data = np.empty(col1.size, dtype=col1.dtype)
            data[:] = col1

        if data.size == 0:
            return

        h5f.create_array('/PRIVATE/INDEX' + cls.group, cls.table_id, obj=data, title=cls.results_type, createparents=True)

    @classmethod
    def _write_index(cls, h5f):

        table = cls.get_table(h5f)

        # noinspection PyProtectedMember
        domain_id = table.cols._f_col('DOMAIN_ID')[:]

        unique, counts = np.unique(domain_id, return_counts=True)
        counts = dict(zip(unique, counts))

        domains = h5f.create_table('/INDEX' + cls.group, cls.table_id, cls.IndexFormat, cls.results_type,
                                   expectedrows=len(counts), createparents=True)

        row = domains.row

        pos = 0

        for i in range(len(counts)):
            d = i + 1
            count = counts[d]

            row['DOMAIN_ID'] = d
            row['POSITION'] = pos
            row['LENGTH'] = count

            row.append()

            pos += count

        domains.flush()
