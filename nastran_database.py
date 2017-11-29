from __future__ import print_function, absolute_import
from six import iteritems, itervalues
from six.moves import range


import tables
import numpy as np

from mrPunch._table_formats.punch_table import PunchTable
from mrPunch._punch_reader import PunchReader
from mrNastran.bdf_reader import BDFReader
# from mrNastran._table_formats import get_table as get_bdf_table
from mrNastran.bdf_data import get_table as get_bdf_table
from mrF06 import F06Reader

from pyNastran.bdf.bdf import BDF


class NastranDatabase(object):
    def __init__(self, h5filename, mode='r'):

        filters = tables.Filters(complib='zlib', complevel=5)

        self.h5f = tables.open_file(h5filename, mode=mode, filters=filters)

        self._tables = set()
        self._unsupported_tables = set()

        self._bdf = None
        self._pch = None
        self._f06 = None

    def close(self):
        try:
            self.h5f.close()
        except Exception:
            pass

    def load_bdf(self, filename):
        if self._bdf is not None:
            raise Exception('BDF already loaded!')

        self._bdf = filename

        self.bdf = BDF(debug=False)
        self.bdf.read_bdf(filename)

        bdf = self.bdf

        assert bdf is not None

        from mrNastran import get_bdf_cards

        cards = get_bdf_cards(bdf)

        tables = set()
        unsupported = []

        card_names = sorted(cards.keys())

        for card_name in card_names:
            table = get_bdf_table(card_name)

            if table is None:
                unsupported.append(card_name)
                continue

            table.write_data(self.h5f, cards[card_name])
            tables.add(table)

        for table in tables:
            table.finalize(self.h5f)

        self._unsupported_cards(unsupported)

        return self.bdf

    def load_punch(self, pchfile):
        if self._bdf is None:
            raise Exception('BDF must be loaded first!')

        if self._f06 is not None:
            raise Exception('F06 has already been loaded.  Cannot load punch file after f06.')

        self._pch = pchfile

        reader = PunchReader(pchfile)
        reader.register_callback(self._load_punch_table)
        reader.read()

        for table in self._tables:
            table.finalize(self.h5f)

        self._tables.clear()
        self._write_unsupported_tables()

    def load_f06(self, f06file):
        if self._bdf is None:
            raise Exception('BDF must be loaded first!')

        if self._pch is not None:
            raise Exception('Punch file has already been loaded.  Cannot load f06 file after punch.')

        self._f06 = f06file

        reader = F06Reader(f06file)
        reader.register_callback(self._load_punch_table)
        reader.read()

        for table in self._tables:
            table.finalize(self.h5f)

        self._tables.clear()

    def _unsupported_cards(self, cards):
        cards = np.array(cards, dtype='S8')
        self.h5f.create_array('/PRIVATE/NASTRAN/INPUT', 'UNSUPPORTED_CARDS', obj=cards, title='UNSUPPORTED BDF CARDS',
                         createparents=True)

    def _unsupported_table(self, table_data):
        print('Unsupported table %s' % table_data.header.results_type)
        self._unsupported_tables.add(table_data.header.results_type)

    def _write_unsupported_tables(self):
        headers = list(sorted(self._unsupported_tables))
        data = np.array(headers, dtype='S256')

        self.h5f.create_array('/PRIVATE/NASTRAN/RESULT', 'UNSUPPORTED_PUNCH_TABLES', obj=data, title='UNSUPPORTED PUNCH TABLES',
                         createparents=True)

    def _load_punch_table(self, table_data):

        print(table_data.header)

        table_format = PunchTable.get_punch_table(table_data.header.results_type, table_data.data)

        if table_format is None:
            return self._unsupported_table(table_data)

        table_format.write_data(self.h5f, table_data)

        self._tables.add(table_format)
