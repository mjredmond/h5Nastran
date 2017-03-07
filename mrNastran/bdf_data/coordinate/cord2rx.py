"""
Copyright (C) Michael James Redmond, Jr - All Rights Reserved
Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Michael James Redmond, Jr.
"""
from __future__ import print_function, absolute_import
from six import iteritems, iterkeys, itervalues
from six.moves import range

from ._cord2 import CORD2

from .._cards import register_card


@register_card
class CORD2RX(CORD2):

    table_reader = CORD2.table_reader.copy()
    table_reader.table_path = '/NASTRAN/INPUT/COORDINATE/CORD2RX'
    table_reader.table_id = 'CORD2RX'

