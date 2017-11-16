"""
"""
from __future__ import print_function, absolute_import
from six import iteritems, iterkeys, itervalues
from six.moves import range

import tables as tb

from .node import GRID
from .coordinate import Cord
from .element import Element
from .property import Property


class BDFData(object):
    def __init__(self):
        self.grid = GRID(self)
        self.cord = Cord(self)
        self.element = Element(self)
        self.property = Property(self)

    def read_h5(self, h5f):
        if isinstance(h5f, str):
            h5f = tb.open_file(h5f, 'r')

        self.grid.read_h5(h5f)
        self.cord.read_h5(h5f)
        self.element.read_h5(h5f)
        self.property.read_h5(h5f)
