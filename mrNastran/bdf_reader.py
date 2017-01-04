"""
Copyright (C) Michael James Redmond, Jr - All Rights Reserved
Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Michael James Redmond, Jr.
"""
from __future__ import print_function, absolute_import
from six import iteritems, itervalues
from six.moves import range

from collections import OrderedDict
import os


from .utilities import convert_field, chunk_string


class BulkData(object):
    def __init__(self):
        self.filename = ''
        self.line_number = 0
        self.data = []
        self.counter = 0

    def convert_data(self):
        if ',' in self.data[0]:
            self._convert_data_2()
        else:
            self._convert_data_1()

    def _convert_data_1(self):
        new_data = []

        for i in range(len(self.data)):
            data_i = self.data[i]
            if i == 0:
                new_data.append(data_i[:8].strip())

            if '*' in data_i:
                width = 16
            else:
                width = 8

            new_data.extend([convert_field(_) for _ in chunk_string(data_i[8:], width)])

        self.data.clear()
        self.data.extend(new_data)

    def _convert_data_2(self):
        new_data = []

        for i in range(len(self.data)):
            data_i = self.data[i]
            tmp = data_i.split(',')
            if i > 0:
                tmp = tmp[1:]
            for _ in tmp:
                new_data.append(convert_field(_))

        self.data.clear()
        self.data.extend(new_data)

    def __str__(self):
        return str((self.filename, self.line_number, self.counter, self.data))


class OtherData(object):
    def __init__(self):
        self.filename = ''
        self.line_number = 0
        self.data = ''
        self.counter = 0

    def __str__(self):
        return str((self.filename, self.line_number, self.counter, self.data))


class BDFData(object):
    def __init__(self):
        self.bulk_data = OrderedDict()
        """:type: dict[str, dict[str, list[BulkData]]]"""

        self.other_data = []
        """:type: list[OtherData]"""


class FileReader(object):
    def __init__(self, filename):
        with open(filename, 'r') as f:
            self.data = f.read().split('\n')
        self.i = -1

    def next_line(self):
        self.i += 1
        try:
            return self.data[self.i]
        except IndexError:
            return None

    def previous_line(self):
        self.i -= 1
        try:
            return self.data[self.i]
        except IndexError:
            return None


class BDFReader(object):
    def __init__(self, filename):
        self.filename = filename

        self.bdf_data = BDFData()

        self._bulk_data = False

        self._counter = 0

        self._enddata = False

        self._read(filename)

    def _read(self, filename):
        reader = FileReader(filename)

        while True:
            data_i = reader.next_line()

            # print(filename, data_i)

            if data_i is None:
                break

            tmp = remove_comments(data_i)

            if tmp.strip() == '':
                continue

            tmp = data_i.strip().upper()

            if tmp.startswith('BEGIN BULK'):
                self._bulk_data = True
                continue
            elif tmp[:7] == 'INCLUDE':
                include_file = get_include_file(reader, remove_comments(data_i), filename)
                self._read(include_file)
                if self._enddata:
                    break
                continue

            tmp = remove_comments(data_i).strip()

            if not self._bulk_data or tmp == '':
                other_data = OtherData()
                other_data.filename = filename
                other_data.line_number = reader.i + 1
                other_data.counter = self._counter
                other_data.data = data_i
                self.bdf_data.other_data.append(other_data)
                self._counter += 1
                continue

            if tmp.startswith('ENDDATA'):
                self._enddata = True
                break

            bulk_data = BulkData()
            bulk_data.filename = filename
            bulk_data.line_number = reader.i + 1

            data = bulk_data.data

            first_line = set_string_width(remove_comments(data_i))

            data.append(first_line)

            while True:
                next_line = reader.next_line()

                if next_line is None:
                    break

                if remove_comments(next_line).strip() == '':
                    continue

                if is_continuation(bulk_data, next_line):
                    data.append(next_line)
                else:
                    reader.previous_line()
                    break

            self._add_bulk_data(bulk_data)

    def _add_bulk_data(self, bulk_data):
        bulk_data.counter = self._counter
        self._counter += 1

        data = bulk_data.data[0]

        if ',' in data:
            tmp = data.split(',')
            card_id = tmp[0].strip().upper()
            _id = tmp[1].strip()
        else:

            card_id = data[:8].strip().upper()

            if '*' in data:
                _id = data[8:24].strip()
            else:
                _id = data[8:16].strip()

        if ',' in data:
            new_data = [_.strip() for _ in bulk_data.data]
        else:
            new_data = [set_string_width(_)[:72] for _ in bulk_data.data]

        bulk_data.data.clear()
        bulk_data.data.extend(new_data)
        bulk_data.convert_data()

        try:
            cards = self.bdf_data.bulk_data[card_id]
        except KeyError:
            cards = self.bdf_data.bulk_data[card_id] = OrderedDict()

        try:
            cards[_id].append(bulk_data)
        except KeyError:
            cards[_id] = [bulk_data]


def is_continuation(bulk_data, next_line):
    data = bulk_data.data

    if ',' in data[-1]:
        tmp = data[-1].strip()
        next_tmp = next_line.strip()

        if tmp.endswith(',') and next_tmp.startswith(','):
            return True
        else:
            return False

    else:
        tmp = set_string_width(data[-1])
        next_tmp = set_string_width(next_line)

        if tmp[72:81].strip() == next_tmp[:8].strip():
            return True
        else:
            return False


def get_include_file(reader, first_line, current_file):
    include_line = first_line

    if include_line.count("'") != 2:
        while True:
            next_line = reader.next_line()
            if next_line is None:
                break
            include_line += remove_comments(next_line)

            if include_line.count("'") == 2:
                break

    include_file = include_line.split("'")[1]

    path = os.path.dirname(current_file)

    return os.path.join(path, include_file)


def remove_comments(line):
    index = line.find(r'$')

    if index < 0:
        index = len(line)
    elif index == 0:
        return ''

    return line[0:index]


def set_string_width(line):
    return '%-80s' % line
