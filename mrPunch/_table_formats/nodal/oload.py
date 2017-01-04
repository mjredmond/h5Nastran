"""
Copyright (C) Michael James Redmond, Jr - All Rights Reserved
Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Michael James Redmond, Jr.
"""
from __future__ import print_function, absolute_import
from six import iteritems, itervalues
from six.moves import range

from .._main import register_table

from .displacement import _Table_0001 as _DisplacementTable


@register_table('OLOADS REAL OUTPUT')
class _Table_0001(_DisplacementTable):
    group = '/NASTRAN/RESULT/NODAL'
    table_id = 'OLOAD'
    table_path = '%s/%s' % (group, table_id)
