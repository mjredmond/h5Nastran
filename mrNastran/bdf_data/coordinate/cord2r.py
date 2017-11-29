from __future__ import print_function, absolute_import
from six import iteritems, iterkeys, itervalues
from six.moves import range

from ._cord2 import Cord2


class CORD2R(Cord2):
    table_reader = Cord2.table_reader.copy()
    table_reader.table_path = '/NASTRAN/INPUT/COORDINATE/CORD2R'
    table_reader.table_id = 'CORD2R'

