from __future__ import print_function, absolute_import
from six import iteritems, iterkeys, itervalues
from six.moves import range


from .grid import GRID


class Node(object):
    def __init__(self, bdf_data):
        self.bdf_data = bdf_data

        self.grid = GRID(self)

    def read_h5(self, h5f):
        self.grid.read_h5(h5f)

