"""
"""
from __future__ import print_function, absolute_import
from six import iteritems, itervalues
from six.moves import range


from ..._main import register_table

from ._strain_energy_table import StrainEnergyTable

@register_table('ELEMENT STRAIN ENERGIES QUAD4 REAL OUTPUT')
class _Table_001(StrainEnergyTable):
    group = StrainEnergyTable.group
    table_id = 'QUAD4'
    table_path = '%s/%s' % (group, table_id)
