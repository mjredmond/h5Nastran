"""
"""
from __future__ import print_function, absolute_import

from nastran_database import NastranDatabase


pchfile = r'./files/wing_punchandpost.pch'
bdffile = r'./files/W1000BOstat.bdf'


db = NastranDatabase(r'./files/W1000BOstat.h5', 'w')


db.read(bdffile)


