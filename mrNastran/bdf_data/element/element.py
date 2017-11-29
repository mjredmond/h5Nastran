from __future__ import print_function, absolute_import
from six import iteritems, iterkeys, itervalues
from six.moves import range


from .cbar import CBAR
from .cbeam import CBEAM
from .cquad4 import CQUAD4
from .ctria3 import CTRIA3


class Element(object):
    def __init__(self, bdf_data):
        self.bdf_data = bdf_data

        self.cbar = CBAR(bdf_data)
        self.cbeam = CBEAM(bdf_data)
        self.cquad4 = CQUAD4(bdf_data)
        self.ctria3 = CTRIA3(bdf_data)

    def read_h5(self, h5f):
        self.cbar.read_h5(h5f)
        self.cbeam.read_h5(h5f)
        self.cquad4.read_h5(h5f)
        self.ctria3.read_h5(h5f)
