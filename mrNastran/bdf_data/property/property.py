"""
Copyright (C) Michael James Redmond, Jr - All Rights Reserved
Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Michael James Redmond, Jr.
"""
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

    def set_pid(self, pid):
        try:
            self.pbar.set_pid(pid)
            self._property = self.pbar
            return
        except ValueError:
            pass

        try:
            self.pbeam.set_pid(pid)
            self._property = self.pbeam
            return
        except ValueError:
            pass

        try:
            self.pshell.set_pid(pid)
            self._property = self.pshell
            return
        except ValueError:
            pass

        raise ValueError('PID %d does not exist!' % pid)
