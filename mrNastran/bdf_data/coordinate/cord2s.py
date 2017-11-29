from __future__ import print_function, absolute_import
from six import iteritems, iterkeys, itervalues
from six.moves import range

import numpy as np
from math import radians, sin, cos

from ._cord2 import Cord2


class CORD2S(Cord2):
    table_reader = Cord2.table_reader.copy()
    table_reader.table_path = '/NASTRAN/INPUT/COORDINATE/CORD2S'
    table_reader.table_id = 'CORD2S'

