from __future__ import print_function, absolute_import
from six import iteritems, iterkeys, itervalues
from six.moves import range


from .mat1 import MAT1
from .mat4 import MAT4
from .mat8 import MAT8


class Material(object):
    def __init__(self, bdf_data):
        self.bdf_data = bdf_data

        self.mat1 = MAT1(bdf_data)
        self.mat4 = MAT4(bdf_data)
        self.mat8 = MAT8(bdf_data)

    def read_h5(self, h5f):
        self.mat1.read_h5(h5f)
        self.mat4.read_h5(h5f)
        self.mat8.read_h5(h5f)

