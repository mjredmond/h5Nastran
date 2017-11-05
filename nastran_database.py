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
import numpy as np

from mrPunch._table_formats import get_table as get_pch_table
from mrPunch._punch_reader import PunchReader
from mrNastran.bdf_reader import BDFReader
# from mrNastran._table_formats import get_table as get_bdf_table
from mrNastran.bdf_data import get_table as get_bdf_table


class NastranDatabase(object):
    def __init__(self, h5filename, mode='r'):

        filters = tables.Filters(complib='zlib', complevel=5)

        self.h5f = tables.open_file(h5filename, mode=mode, filters=filters)

        self._tables = set()

    def close(self):
        try:
            self.h5f.close()
        except Exception:
            pass

    def _callback(self, table_data):
        table_format = get_pch_table(table_data.header.results_type)

        if table_format is None:
            return self._unsupported_table(table_data)

        table_format.write_data(self.h5f, table_data)

        self._tables.add(table_format)

    def read(self, bdffile, pchfile=None):
        bdf_data = self._read_bdf(bdffile)

        if pchfile is not None:
            self._read_pch(pchfile)

        return bdf_data

    def _read_bdf(self, bdffile):
        reader = BDFReader(bdffile)

        bulk_data = reader.bdf_data.bulk_data

        cards = sorted(bulk_data.keys())

        tables = set()
        unsupported = []

        for card in cards:

            # if card != 'GRID':
            #     continue

            table = get_bdf_table(card)

            if table is None:
                unsupported.append(card)
                continue

            table.write_data(self.h5f, bulk_data[card])

            tables.add(table)

        for table in tables:
            table.finalize(self.h5f)

        self._unsupported_cards(unsupported)

        return reader.bdf_data

    def _unsupported_cards(self, cards):
        cards = np.array(cards, dtype='S8')
        self.h5f.create_array('/PRIVATE/NASTRAN/INPUT', 'UNSUPPORTED_CARDS', obj=cards, title='UNSUPPORTED BDF CARDS',
                         createparents=True)

    def _read_pch(self, pchfile):
        reader = PunchReader(pchfile)
        reader.register_callback(self._callback)
        reader.read()

        for table in self._tables:
            table.finalize(self.h5f)

        self._tables.clear()

    def _unsupported_table(self, table_data):
        print('Unsupported table %s' % str(table_data.header))
