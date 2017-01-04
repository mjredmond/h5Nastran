"""
Copyright (C) Michael James Redmond, Jr - All Rights Reserved
Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Michael James Redmond, Jr.
"""
from __future__ import print_function, absolute_import
from six import iteritems, itervalues
from six.moves import range


from ..._main import register_table

from ._strain_energy_table import StrainEnergyTable

@register_table('ELEMENT STRAIN ENERGIES BAR REAL OUTPUT')
class _Table_001(StrainEnergyTable):
    group = StrainEnergyTable.group
    table_id = 'BAR'
    table_path = '%s/%s' % (group, table_id)
