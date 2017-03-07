"""
Copyright (C) Michael James Redmond, Jr - All Rights Reserved
Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Michael James Redmond, Jr.
"""
from __future__ import print_function, absolute_import
from six import iteritems, iterkeys, itervalues
from six.moves import range

from mrNastran.bdf_data import BDFData


bdf_data = BDFData()
bdf_data.read_h5('./files/W1000BOstat.h5')

print(bdf_data.grid.data)
print(bdf_data.cord.cord2r.data)