from __future__ import print_function, absolute_import
from six import iteritems, iterkeys, itervalues
from six.moves import range


from .rbe2 import RBE2
from .rbe3 import RBE3


class RigidElement(object):
    def __init__(self, bdf_data):
        self.bdf_data = bdf_data

        self.rbe2 = RBE2(bdf_data)
        self.rbe3 = RBE3(bdf_data)

    def read_h5(self, h5f):
        self.rbe2.read_h5(h5f)
        self.rbe3.read_h5(h5f)
