"""
Copyright (C) Michael James Redmond, Jr - All Rights Reserved
Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Michael James Redmond, Jr.
"""
from __future__ import print_function, absolute_import
from six import iteritems, itervalues
from six.moves import range

from ._file_reader import FileReader
from ._table_data import TableData


def _default_callback(table_data):
    print(table_data.header)


class PunchReader(object):
    def __init__(self, filename):
        self.file = FileReader(filename)

        self._done_reading = False

        self._callback = _default_callback

    def register_callback(self, callback):
        assert callable(callback)

        self._callback = callback

    def close(self):
        self.file.close()

    def read(self):
        while not self._done_reading:
            table_data, line_number = self._read_table()

            try:
                table_data = TableData(table_data)
            except TypeError:
                break

            table_data.header.lineno = line_number

            self._callback(table_data)

    def _read_table(self):

        table_data = []

        reading_data = False

        line_number = -1

        while True:
            next_line = self.file.next_line()

            if next_line is None:
                self._done_reading = True
                break

            if next_line.strip() == b'':
                break

            first_char = chr(next_line[0])

            if first_char == '$' and reading_data:
                self.file.previous_line()
                reading_data = False
                break

            if first_char != '$':
                reading_data = True

            if first_char == '-':
                try:
                    table_data[-1] += next_line[18:]
                except IndexError:
                    raise Exception('Error reading punch file %s!' % self.file.filename)

            else:
                if len(table_data) == 0:
                    line_number = self.file.line_number()

                table_data.append(next_line)

        if len(table_data) == 0:
            return None

        return table_data, line_number
