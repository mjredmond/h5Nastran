This repository will be renamed to h5Nastran in the near future.

h5Nastran is a python package that deals with the MSC.Nastran h5 file format.  It uses pyNastran to convert bdf files to the h5 format, and has a standalone punch and f06 results reader to convert to the h5 format.  Results tables are easily searchable.

Example:
```python
from h5Nastran import H5Nastran

db = H5Nastran('db.h5', 'w')
db.load_bdf('some.bdf')
db.load_punch('some.pch')

domain_ids = [0, 1, 2, 3]
elements = [1, 2, 3, 4, 5, 6, 7]
quad4_loads = db.result.elemental.element_force.quad4.search(domain_ids, elements)
```


Not all bdf features are currently supported.  Bulk data cards are pretty easy to add... either make a pull request or request one to be added.  Punch tables are also easy to add - either make a pull request or request one to be added (but please provide an example of the punch table format).

bdf's, punch files, and f06 files are appreciated so I can add more support and do more testing.  The punch file reader is currently much better supported than the f06 file reader.
