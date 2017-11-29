import numpy as np
from six import add_metaclass


_cards = {}
_card_tables = {}


def _register_card(cls):
    try:
        card_type = cls.table_reader.card_type
    except AttributeError:
        card_type = cls.__name__

    _cards[card_type] = cls
    _card_tables[card_type] = cls.table_reader
    return cls


def get_card(card_name):
    return _cards.get(card_name, None)


def get_table(card_name):
    return _card_tables.get(card_name, None)


class RegisterClass(type):
    def __new__(cls, clsname, bases, attrs):
        newclass = super(RegisterClass, cls).__new__(cls, clsname, bases, attrs)
        _register_card(newclass)
        return newclass


@add_metaclass(RegisterClass)
class AbstractCard(object):
    table_reader = None
    dtype = None
    _id = None

    def __init__(self, bdf_data):
        self.bdf_data = bdf_data
        self.data = np.zeros(0, dtype=self.dtype)

    def read_h5(self, h5f):
        self.set_data(self.table_reader.read(h5f))

    def resize(self, new_size):
        self.data.resize(new_size)

    def set_data(self, data):
        self.resize(data.size)
        np.copyto(self.data, data)

