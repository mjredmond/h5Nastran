"""
"""
from __future__ import print_function, absolute_import
from six import iteritems, iterkeys, itervalues
from six.moves import range

import numpy as np
from math import radians, sin, cos

from ._cord2 import Cord2

from .._cards import register_card


@register_card
class CORD2C(Cord2):

    table_reader = Cord2.table_reader.copy()
    table_reader.table_path = '/NASTRAN/INPUT/COORDINATE/CORD2C'
    table_reader.table_id = 'CORD2C'

    def to_reference_coord(self, cid, x):
        self.set_cid(cid)

        data = self._current_data_1
        v1, v2, v3 = self._current_data_2

        r, t, z = x

        t = radians(t)

        x = [r * cos(t), r * sin(t), z]

        xp = [np.dot(x, v1), np.dot(x, v2), np.dot(x, v3)]

        return xp + data[2]


