
from __future__ import print_function, absolute_import
from six import iteritems, iterkeys, itervalues
from six.moves import range

try:
    from ._file_reader import FileReader
except Exception:
    from _file_reader import FileReader


class F06Table(object):
    def __init__(self):
        self.header = []
        self.data = []
        self.line_number = -1
        self.table_format = None


class TableFormat(object):
    def __init__(self):
        self.header_check = b'D I S P L A C E M E N T   V E C T O R'
        self.header_check_line = 2
        self.header_lines = 5


class F06Reader(object):
    def __init__(self, filename):
        self.file = FileReader(filename)

        self._done_reading = False

        self._table_formats = [TableFormat()]

        self._current_table = None

    def read(self):
        while not self._done_reading:
            table_lines, line_number = self._read_table()
            if self._done_reading:
                break

            table_format = self._find_table_format(table_lines)

            if table_format is None:
                continue

            table = F06Table()
            table.header.extend(table_lines[:table_format.header_lines])
            table.data.extend(table_lines[table_format.header_lines:])

            if self._current_table is None:
                self._current_table = table
            else:
                if self._current_table.header == table.header:
                    self._current_table.data.extend(table.data)
                else:
                    self._current_table.table_format = table_format
                    self._process_table(self._current_table)
                    self._current_table = table

        if self._current_table is not None:
            self._process_table(self._current_table)
            self._current_table = None

    def _process_table(self, table):
        print(table.header)

    def _find_table_format(self, table_lines):
        for format in self._table_formats:
            if format.header_check in table_lines[format.header_check_line]:
                return format

        return None

    def _read_table(self):
        table_lines = []

        first_line = self._find_next_table()
        if self._done_reading:
            return None, None

        line_number = self.file.line_number()

        while True:
            if first_line is not None:
                line = first_line
                first_line = None
            else:
                line = self.file.next_line()

            self._check_done_reading(line)
            if self._done_reading:
                break

            # print(line)

            if line.startswith(b'1'):
                break

            table_lines.append(line)

        return table_lines, line_number

    def _find_next_table(self):
        while True:
            line = self.file.next_line()
            self._check_done_reading(line)
            if self._done_reading:
                break

            if line.startswith(b'0') and b'SUBCASE' in line:
                return line

        return None

    def _check_done_reading(self, line):
        if line is None or b'END OF JOB' in line:
            self._done_reading = True

