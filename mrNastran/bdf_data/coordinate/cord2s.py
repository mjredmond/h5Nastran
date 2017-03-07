"""
Copyright (C) Michael James Redmond, Jr - All Rights Reserved
Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Michael James Redmond, Jr.
"""
from __future__ import print_function, absolute_import
from six import iteritems, iterkeys, itervalues
from six.moves import range

import numpy as np
from math import radians, sin, cos

from ._cord2 import CORD2

from .._cards import register_card


@register_card
class CORD2S(CORD2):

    table_reader = CORD2.table_reader.copy()
    table_reader.table_path = '/NASTRAN/INPUT/COORDINATE/CORD2S'
    table_reader.table_id = 'CORD2S'

    def to_reference_coord(self, cid, x):
        self.set_cid(cid)

        data = self._current_data_1
        v1, v2, v3 = self._current_data_2

        r, theta, phi = x

        theta = radians(theta)
        phi = radians(phi)

        sin_phi = sin(phi)

        x = [r * sin_phi * cos(theta), r * sin_phi * sin(theta), r * cos(phi)]

        xp = [np.dot(x, v1), np.dot(x, v2), np.dot(x, v3)]

        return xp + data[2]
