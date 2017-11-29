from __future__ import print_function, absolute_import
from six import iteritems, iterkeys, itervalues
from six.moves import range

from mrF06 import F06Reader
from nastran_database import NastranDatabase

import re


filename = r'file.f06'
bdffile = r'file.bdf'

# f = F06Reader(filename)

# f.read()

db = NastranDatabase('test.h5', 'w')
db.load_bdf(bdffile)


# db.load_f06(filename)

