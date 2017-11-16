"""
"""
from __future__ import print_function, absolute_import
from six import iteritems, itervalues
from six.moves import range

from ..._main import register_table

from tables import IsDescription, Int64Col, Float64Col, StringCol
import tables

from ...abstract_table import AbstractTable

from ._shell import ShellTable


@register_table('ELEMENT FORCES 74 TRIA3 REAL OUTPUT MATERIAL')
@register_table('ELEMENT FORCES 74 TRIA3 REAL OUTPUT')
class _Table_0001(ShellTable):

    group = '/NASTRAN/RESULT/ELEMENTAL/FORCE'
    table_id = 'TRIA3'
    table_path = '%s/%s' % (group, table_id)
