"""
"""
from __future__ import print_function, absolute_import
from six import iteritems, itervalues
from six.moves import range


from mrNastran.bdf_reader import BDFReader


reader = BDFReader('./files/wing.bdf')


for card_id, item in iteritems(reader.bdf_data.bulk_data):
    if card_id != 'PARAM':
        continue
    for card_key, card_data in iteritems(item):
        print(card_data[0])
