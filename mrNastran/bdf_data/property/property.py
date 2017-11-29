from __future__ import print_function, absolute_import
from six import iteritems, iterkeys, itervalues
from six.moves import range


from .pbar import PBAR
from .pshell import PSHELL
from .pbeam import PBEAM


class Property(object):
    def __init__(self, bdf_data):
        self.bdf_data = bdf_data

        self.pbar = PBAR(bdf_data)
        self.pbeam = PBEAM(bdf_data)
        self.pshell = PSHELL(bdf_data)

        self._property = None

    def read_h5(self, h5f):
        self.pbar.read_h5(h5f)
        self.pbeam.read_h5(h5f)
        self.pshell.read_h5(h5f)

