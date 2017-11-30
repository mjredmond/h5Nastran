from __future__ import print_function, absolute_import
from six import iteritems, iterkeys, itervalues
from six.moves import range


from .force import FORCE
from .moment import MOMENT


class Load(object):
    def __init__(self, bdf_data):
        self.bdf_data = bdf_data

        self.force = FORCE(bdf_data)
        self.moment = MOMENT(bdf_data)

    def read_h5(self, h5f):
        self.force.read_h5(h5f)
        self.moment.read_h5(h5f)

