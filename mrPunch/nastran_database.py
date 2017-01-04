"""
Copyright (C) Michael James Redmond, Jr - All Rights Reserved
Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Michael James Redmond, Jr.
"""
from __future__ import print_function, absolute_import
from six import iteritems, itervalues
from six.moves import range


import tables

from ._table_formats import get_table
from ._punch_reader import PunchReader


class NastranDatabase(object):
    def __init__(self, h5filename, mode='r'):

        filters = tables.Filters(complib='zlib', complevel=5)

        self.h5f = tables.open_file(h5filename, mode=mode, filters=filters)

        self._tables = set()

    def _callback(self, table_data):
        table_format = get_table(table_data.header.results_type)

        if table_format is None:
            return self._unsupported_table(table_data)

        table_format.write_data(self.h5f, table_data)

        self._tables.add(table_format)

    def read(self, pchfile):
        reader = PunchReader(pchfile)
        reader.register_callback(self._callback)
        reader.read()

        for table in self._tables:
            table.finalize(self.h5f)

        self._tables.clear()

    def _unsupported_table(self, table_data):
        print('Unsupported table %s' % str(table_data.header))
