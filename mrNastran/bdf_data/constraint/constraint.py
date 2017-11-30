from __future__ import print_function, absolute_import
from six import iteritems, iterkeys, itervalues
from six.moves import range


from .spc1 import SPC1


class Constraint(object):
    def __init__(self, bdf_data):
        self.bdf_data = bdf_data

        self.spc1 = SPC1(self)

    def read_h5(self, h5f):
        self.spc1.read_h5(h5f)

