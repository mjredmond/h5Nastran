"""
Copyright (C) Michael James Redmond, Jr - All Rights Reserved
Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Michael James Redmond, Jr.
"""
from __future__ import print_function, absolute_import
from six import iteritems, itervalues
from six.moves import range


cards = {}
card_tables = {}


def register_card(cls):
    cards[cls.__name__] = cls
    card_tables[cls.__name__] = cls.table_reader
    return cls


def get_card(card_name):
    return cards.get(card_name, None)


def get_table(card_name):
    return card_tables.get(card_name, None)
