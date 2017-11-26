from __future__ import print_function, absolute_import
from six import iteritems, iterkeys, itervalues
from six.moves import range

from f06_reader import F06Reader

import re


filename = r'../files/static_solid_shell_bar_xyz.f06'

f = F06Reader(filename)

f.read()

