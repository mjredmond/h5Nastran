from __future__ import print_function

from h5Nastran import H5Nastran

db = H5Nastran('db.h5', 'w')
db.load_bdf('some.bdf')
db.load_punch('some.pch')

domain_ids = [1, 2, 3]
elements = [1, 2, 3, 4, 5, 6, 7]
quad4_loads = db.result.elemental.element_force.quad4.search(domain_ids, elements)

print(quad4_loads)


