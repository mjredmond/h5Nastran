
from __future__ import print_function, absolute_import
from six import iteritems, iterkeys, itervalues
from six.moves import range


import tables
import numpy as np


class PunchTable(object):
    
    def __init__(self, results_type, group, table_id, index_columns, dtype, data_indices, validator=None, index_format_dtype=None):
        self.results_type = results_type
        self.group = group
        self.table_id = table_id
        self.table_path = '%s/%s' % (self.group, self.table_id)
        self.index_columns = tuple(index_columns)
        self.dtype = np.dtype(dtype)

        self.Format = tables.descr_from_dtype(self.dtype)

        self.data_indices = tuple(data_indices)

        self.validator = validator
        
        if index_format_dtype is None:
            class IndexFormat(tables.IsDescription):
                DOMAIN_ID = tables.Int64Col(pos=1)
                POSITION = tables.Int64Col(pos=2)
                LENGTH = tables.Int64Col(pos=3)
            self.index_format_dtype = tables.dtype_from_descr(IndexFormat)
        else:
            self.index_format_dtype = np.dtype(index_format_dtype)
            IndexFormat = tables.descr_from_dtype(self.index_format_dtype)
            
        self.IndexFormat = IndexFormat
        
        self.domain_count = 0

    def write_data(self, h5f, data):
        self.domain_count += 1

        h5ftable = self.get_table(h5f)

        data = self.to_numpy(data)

        h5ftable.append(data)

        h5f.flush()

    def to_numpy(self, data):
        names = self.dtype.names

        result = np.empty(len(data), dtype=self.dtype)

        _result = {name: result[name] for name in names}

        indices = self.data_indices

        for i in range(len(data)):
            _data = data[i]
            for j in range(len(names)):
                _result[names[j]][i] = _data[indices[j]]

            try:
                self.validator(data[i])
            except TypeError:
                pass

        return result

    def get_table(self, h5f, expected_rows=1000000):
        try:
            return h5f.get_node(self.table_path)
        except tables.NoSuchNodeError:
            return h5f.create_table(self.group, self.table_id, self.Format, self.results_type,
                                    expectedrows=expected_rows, createparents=True)

    def finalize(self, h5f):
        self._write_index(h5f)
        self._write_private_index(h5f)

    def _write_private_index(self, h5f):
        table = self.get_table(h5f)

        # noinspection PyProtectedMember
        col1 = table.cols._f_col(self.index_columns[0])[:]

        try:
            # noinspection PyProtectedMember
            col2 = table.cols._f_col(self.index_columns[1])[:]
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

        h5f.create_array('/PRIVATE/INDEX' + self.group, self.table_id, obj=data, title=self.results_type, createparents=True)

    def _write_index(self, h5f):

        table = self.get_table(h5f)

        # noinspection PyProtectedMember
        domain_id = table.cols._f_col('DOMAIN_ID')[:]

        unique, counts = np.unique(domain_id, return_counts=True)
        counts = dict(zip(unique, counts))

        domains = h5f.create_table('/INDEX' + self.group, self.table_id, self.IndexFormat, self.results_type,
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


if __name__ == '__main__':

    table = PunchTable(
        'some result',
        'some group',
        'some id',
        ['ID'],
        [('ID', 'i8'), ('fx', 'f8'), ('fy', 'f8'), ('fz', 'f8'), ('m', 'f8', (3,))],
        [0, 2, 3, 4, slice(5, 8), slice(8, 11)]
    )

    data = [
        [1, '', 1., 2., 3., 4., 5., 6.],
        [2, '', 1., 2., 3., 4., 5., 6.],
        [3, '', 1., 2., 3., 4., 5., 6.],
        [4, '', 1., 2., 3., 4., 5., 6.],
    ]

    print(table.to_numpy(data))
