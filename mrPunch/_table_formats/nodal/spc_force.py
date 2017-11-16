"""
"""
from __future__ import print_function, absolute_import
from six import iteritems, itervalues
from six.moves import range

from .._main import register_table

from .displacement import _Table_0001 as _DisplacementTable


@register_table('SPCF REAL OUTPUT')
class _Table_0001(_DisplacementTable):
    group = '/NASTRAN/RESULT/NODAL'
    table_id = 'SPC_FORCE'
    table_path = '%s/%s' % (group, table_id)
