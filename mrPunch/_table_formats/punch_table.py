from __future__ import print_function, absolute_import
from six import iteritems, iterkeys, itervalues
from six.moves import range

import tables
import numpy as np
from collections import OrderedDict


class _Format(object):
    def __init__(self):
        raise NotImplementedError


class IndexFormat(tables.IsDescription):
    DOMAIN_ID = tables.Int64Col(pos=1)
    POSITION = tables.Int64Col(pos=2)
    LENGTH = tables.Int64Col(pos=3)


class PrivateIndexFormat(tables.IsDescription):
    LOCATION = tables.Int64Col(pos=1)
    LENGTH = tables.Int64Col(pos=2)
    OFFSET = tables.Int64Col(pos=3)


private_index_format_dtype = tables.dtype_from_descr(PrivateIndexFormat)


class PrivateIndexDataFormat(tables.IsDescription):
    ID = tables.Int64Col(pos=1)


def _validator(data):
    return data


class PunchTable(object):
    _tables = {}

    def __new__(cls, results_type, table_id, group, index_id, dtype, indices, validator=None):
        instance = super(PunchTable, cls).__new__(cls)
        cls._tables[results_type] = instance
        return instance

    @classmethod
    def get_punch_table(cls, results_type, data):
        return cls._tables.get(results_type, None)

    def __init__(self, group, table_id, results_type, index_id, dtype, indices, validator=None):
        self.group = group
        self.table_id = table_id
        self.table_path = '%s/%s' % (group, table_id)
        self.results_type = results_type
        self.index_id = index_id
        self.domain_count = 0

        self.dtype = np.dtype(dtype)

        self.Format = tables.descr_from_dtype(self.dtype)[0]

        self.indices = list(indices)

        if validator is None:
            validator = _validator

        self.validator = validator

        assert len(self.indices) == len(self.dtype.names) - 1

        self.IndexFormat = IndexFormat
        self.PrivateIndexFormat = PrivateIndexFormat
        self.PrivateIndexDataFormat = PrivateIndexDataFormat

        self._index_table = None
        self._private_index_table = None

        self._index_data = []
        self._subcase_index = []
        self._index_offset = 0

    def copy(self):
        from copy import copy
        _copy = copy(self)
        _copy.domain_count = 0
        _copy._index_offset = 0
        del _copy._index_data[:]
        del _copy._subcase_index[:]
        _copy._index_table = None
        _copy._private_index_table = None
        return _copy

    def search_table(self, h5f, domains, data_ids, filter=None):
        private_index_table = self._get_private_index_table(h5f)

        indices = set()

        for domain in domains:
            try:
                index_dict, offset = private_index_table[domain]
            except IndexError:
                continue

            for data_id in data_ids:
                _indices = index_dict[data_id]
                indices.update(set(index + offset for index in _indices))

        results = self.read_table(h5f, sorted(indices))

        if filter is not None:
            indices = set()
            for key in filter.keys():
                data = set(filter[key])
                results_data = results[key]
                for i in range(results_data.shape[0]):
                    if results_data[i] in data:
                        indices.add(i)
            results = results[sorted(indices)]

        return results

    def _get_index_table(self, h5f):
        if self._index_table is None:
            index_table = h5f.get_node('/INDEX%s' % self.table_path)
            index_table = index_table.read()

            self._index_table = [
                set(range(index_table['POSITION'][i], index_table['POSITION'][i] + index_table['LENGTH'][i]))
                for i in range(index_table.shape[0])
            ]

        return self._index_table

    def _get_private_index_table(self, h5f):
        if self._private_index_table is None:
            data = h5f.get_node(self._private_index_path + '/DATA')
            data = data.read()

            identity = h5f.get_node(self._private_index_path + '/IDENTITY')
            identity = identity.read()

            private_index_table = self._private_index_table = []

            _index_data = {}

            for i in range(identity.shape[0]):
                location, length, offset = identity[i]

                try:
                    private_index_table.append(_index_data[location])
                except KeyError:
                    _data = data['ID'][location: location + length]
                    _data_dict = {}
                    for j in range(_data.shape[0]):
                        _data_id = int(_data[j])
                        try:
                            _data_dict[_data_id].append(j)
                        except KeyError:
                            _data_dict[_data_id] = [j]
                    _index_data[location] = (_data_dict, offset)
                    private_index_table.append(_index_data[location])

        return self._private_index_table

    def read_table(self, h5f, indices):
        table = h5f.get_node(self.table_path)

        indices = np.array(indices, dtype='i8')

        data = np.empty(len(indices), dtype=table._v_dtype)
        table._read_elements(indices, data)

        return data

    def write_data(self, h5f, table_data):
        self.domain_count += 1

        h5table = self.get_table(h5f)

        data = self.to_numpy(table_data.data)

        h5table.append(data)

        self._record_data_indices(data)

        h5f.flush()

    def _record_data_indices(self, data):
        index_data = data[self.index_id][:]

        found_index = False

        index_data_offset = 0

        for i in range(len(self._index_data)):
            _index_data = self._index_data[i]
            if _index_data.shape == index_data.shape:
                if np.all(_index_data == index_data):
                    self._subcase_index.append((index_data_offset, index_data.shape[0], self._index_offset))
                    found_index = True
                    break
            index_data_offset += _index_data.shape[0]

        if not found_index:
            self._index_data.append(index_data)
            self._subcase_index.append((index_data_offset, index_data.shape[0], self._index_offset))

        self._index_offset += data.shape[0]

    def to_numpy(self, data):
        result = np.empty(len(data), dtype=self.dtype)

        validator = self.validator

        names = list(self.dtype.names)

        _result = {name: result[name] for name in names}

        for i in range(len(data)):
            _data = data[i]
            _data = validator([_get_data(_data, index) for index in self.indices])
            _data.append(self.domain_count)

            for j in range(len(names)):
                _result[names[j]][i] = _data[j]

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

    @property
    def _private_index_path(self):
        return '/PRIVATE/INDEX' + self.table_path

    def _get_private_index_tables(self, h5f):
        try:
            print(self._private_index_path)
            identity = h5f.get_node(self._private_index_path + '/IDENTITY')
        except tables.NoSuchNodeError:
            identity = h5f.create_table(self._private_index_path, 'IDENTITY', self.PrivateIndexFormat, 'Private Index',
                                        expectedrows=len(self._subcase_index), createparents=True)
        try:
            data = h5f.get_node(self._private_index_path + '/DATA')
        except tables.NoSuchNodeError:
            data = h5f.create_table(self._private_index_path, 'DATA', self.PrivateIndexDataFormat, 'Private Index Data',
                                    expectedrows=sum([len(_) for _ in self._index_data]), createparents=True)

        return identity, data

    def _write_private_index(self, h5f):
        identity, data = self._get_private_index_tables(h5f)

        identity.append(np.array(self._subcase_index, dtype=private_index_format_dtype))

        for index_data in self._index_data:
            data.append(index_data)

        h5f.flush()

        self._private_index_table = None

        del self._subcase_index[:]
        del self._index_data[:]

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

        self._index_table = None


class DefinedValue(object):
    def __init__(self, value):
        self.value = value


def _get_data(data, index):
    if isinstance(index, (int, slice)):
        return data[index]
    elif isinstance(index, (list, tuple)):
        return [_get_data(data, i) for i in index]
    elif isinstance(index, DefinedValue):
        return index.value
    else:
        raise TypeError('Unknown index type! %s' % str(type(index)))


def _validator1(data):
    if data[1] == b'':
        data[1] = 0

    eids = {
        b'F-OF-SPC': -1,
        b'F-OF-MPC': -2,
        b'APP-LOAD': -3,
        b'*TOTALS*': -4
    }

    data[1] = eids.get(data[2].strip(), data[1])

    return data


a = PunchTable(
    '/NASTRAN/RESULT/NODAL', 'GRID_FORCE', 'GRID POINT FORCE BALANCE REAL OUTPUT', 'ID',
    [('ID', 'i8'), ('EID', 'i8'), ('ELNAME', 'S18'), ('F1', 'f8'), ('F2', 'f8'), ('F3', 'f8'),
     ('M1', 'f8'), ('M2', 'f8'), ('M3', 'f8'), ('DOMAIN_ID', 'i8')],
    [0, 2, 3, 5, 6, 7, 8, 9, 10],
    validator=_validator1,
)

if __name__ == '__main__':
    def _validator(data):
        if data[1] == b'':
            data[1] = 0

        eids = {
            b'F-OF-SPC': -1,
            b'F-OF-MPC': -2,
            b'APP-LOAD': -3,
            b'*TOTALS*': -4
        }

        data[1] = eids.get(data[2].strip(), data[1])

        return data


    import tables

    h5f = tables.open_file(r'somefile.h5', 'r')

    a = PunchTable(
        '/NASTRAN/RESULT/NODAL', 'GRID_FORCE', 'GRID POINT FORCE BALANCE REAL OUTPUT', ['ID', 'EID'],
        [('ID', 'i8'), ('EID', 'i8'), ('ELNAME', 'S18'), ('F1', 'f8'), ('F2', 'f8'), ('F3', 'f8'),
         ('M1', 'f8'), ('M2', 'f8'), ('M3', 'f8'), ('DOMAIN_ID', 'i8')],
        [0, 2, 3, 5, 6, 7, 8, 9, 10],
        validator=_validator,
    )

    # results = a.search_table_union(h5f, [0, 1, 2, 3], [
    #     [1000000, ], [1001238, ]
    # ])

    results = a.read_table(h5f, range(0, 1000000, 2))

    print(results)

    from mrPunch._table_formats.punch_table import a as grid_point_force_table

    import tables

    h5f = tables.open_file(r'somefile.h5')

    # data = grid_point_force_table.search_table(h5f, [i for i in range(1000)], [1000000, 1000001],
    #                                            filter={'EID': [1001224, 1001238]})

    # print(data)

    # h5f.close()

    import numpy as np


    def get_data(identity, data, index):
        location, length, offset = identity[index]
        data = data[location: location + length]

        return data


    def get_data_dict(data):
        from collections import OrderedDict
        data_dict = OrderedDict()

        for i in range(data.shape[0]):
            data_id = int(data[i])
            try:
                data_dict[data_id].append(i)
            except KeyError:
                data_dict[data_id] = [i]

        return data_dict


    def serialize_data_dict(data_dict):
        data = []

        for key, _data in data_dict.items():
            _data_ = [key, len(_data)]
            _data_.extend(_data)
            data.extend(_data_)

        return np.array(data)


    def load_data_dict(serialize_data):
        data_dict = {}

        last_i = serialize_data.shape[0] - 1

        i = 0
        while True:
            data_id = serialize_data[i]
            data_len = serialize_data[i + 1]

            _data = serialize_data[i + 2: i + 2 + data_len]

            data_dict[data_id] = _data

            i += 2 + data_len

            if i >= last_i:
                break

        assert i == last_i + 1

        return data_dict


    identity = h5f.get_node('/PRIVATE/INDEX/NASTRAN/RESULT/NODAL/GRID_FORCE/IDENTITY').read()
    data = h5f.get_node('/PRIVATE/INDEX/NASTRAN/RESULT/NODAL/GRID_FORCE/DATA').read()['ID']

    import time

    data_dicts = []

    locs = set()

    time_elapsed = 0

    for i in range(381):
        location = identity['LOCATION'][i]

        if location in locs:
            continue

        data_ = get_data(identity, data, i)

        t1 = time.time()
        data_dict = get_data_dict(data_)
        t2 = time.time()

        time_elapsed += t2 - t1

        location = identity['LOCATION'][i]

        locs.add(location)

        data_dicts.append((location, data_dict))

    print(time_elapsed)

    serialize_data = {}

    for location, data_dict in data_dicts:
        if location not in serialize_data:
            serialize_data[location] = serialize_data_dict(data_dict)

    loaded_data = {}

    locs = set()

    time_elapsed = 0

    for i in range(381):
        location = identity['LOCATION'][i]

        if location in locs:
            continue

        data_ = get_data(identity, data, i)
        location = identity['LOCATION'][i]

        locs.add(location)

        if location not in loaded_data:
            t1 = time.time()
            loaded_data[location] = load_data_dict(serialize_data[location])
            t2 = time.time()
            time_elapsed += t2 - t1

    print(time_elapsed)


