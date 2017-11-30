from __future__ import print_function, absolute_import
from six import iteritems, iterkeys, itervalues
from six.moves import range


from .pcomp import PCOMP
from .pbar import PBAR
from .pbarl import PBARL
from .pbeam import PBEAM
from .pbeaml import PBEAML
from .pbush import PBUSH
from .prod import PROD
from .pshear import PSHEAR
from .pshell import PSHELL


class Property(object):
    def __init__(self, bdf_data):
        self.bdf_data = bdf_data

        self.pcomp = PCOMP(bdf_data)
        self.pbar = PBAR(bdf_data)
        self.pbarl = PBARL(bdf_data)
        self.pbeam = PBEAM(bdf_data)
        self.pbeaml = PBEAML(bdf_data)
        self.pbush = PBUSH(bdf_data)
        self.prod = PROD(bdf_data)
        self.pshear = PSHEAR(bdf_data)
        self.pshell = PSHELL(bdf_data)

    def read_h5(self, h5f):
        self.pcomp.read_h5(h5f)
        self.pbar.read_h5(h5f)
        self.pbarl.read_h5(h5f)
        self.pbeam.read_h5(h5f)
        self.pbeaml.read_h5(h5f)
        self.pbush.read_h5(h5f)
        self.prod.read_h5(h5f)
        self.pshear.read_h5(h5f)
        self.pshell.read_h5(h5f)
