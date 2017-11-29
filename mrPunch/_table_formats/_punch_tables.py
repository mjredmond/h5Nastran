from __future__ import print_function, absolute_import
from six import iteritems, iterkeys, itervalues
from six.moves import range

from .punch_table import PunchTable, DefinedValue


def _default_validator(data):
    return data


# data types

_int = '<i8'
_float = '<f8'
_str18 = 'S18'
_str4 = 'S4'


####################### nodal #######################

# displacement

disp_dtype = [('ID', _int), ('VALUE', _float, (6,)), ('DOMAIN_ID', _int)]

PunchTable('DISPLACEMENTS REAL OUTPUT', 'DISPLACEMENT', '/NASTRAN/RESULT/NODAL', 'ID',
    disp_dtype,
    [0, slice(2, 8)],
    validator=_default_validator,
)


# mpcf

PunchTable('MPCF REAL OUTPUT', 'MPCF', '/NASTRAN/RESULT/NODAL', 'ID',
    disp_dtype,
    [0, slice(2, 8)],
    validator=_default_validator,
)


# oload

PunchTable('OLOADS REAL OUTPUT', 'OLOAD', '/NASTRAN/RESULT/NODAL', 'ID',
    disp_dtype,
    [0, slice(2, 8)],
    validator=_default_validator,
)


# spcforce

PunchTable('SPCF REAL OUTPUT', 'SPC_FORCE', '/NASTRAN/RESULT/NODAL', 'ID',
    disp_dtype,
    [0, slice(2, 8)],
    validator=_default_validator,
)


# grid_force

def _validator(data):
    if data[1] == b'':
        data[1] = 0

    eids = {
        b'F-OF-SPC': -1,
        b'F-OF-MPC': -2,
        b'APP-LOAD': -3,
        b'*TOTALS*': -4
    }

    data[1] = eids.get(data[2].strip(), data[1])

    return data


PunchTable('GRID POINT FORCE BALANCE REAL OUTPUT', 'GRID_FORCE', '/NASTRAN/RESULT/NODAL', 'ID',
    [('ID', _int), ('EID', _int), ('ELNAME', _str18), ('F1', _float), ('F2', _float), ('F3', _float),
     ('M1', _float), ('M2', _float), ('M3', _float), ('DOMAIN_ID', _float)],
    [0, 2, 3, 5, 6, 7, 8, 9, 10],
    validator=_validator,
)


####################### elemental force #######################

# bar

PunchTable('ELEMENT FORCES 34 BAR REAL OUTPUT', 'BAR', '/NASTRAN/RESULT/ELEMENTAL/FORCE', 'EID',
    [('EID', _int), ('M1A', _float), ('M2A', _float), ('M1B', _float), ('M2B', _float), ('SHR1', _float),
     ('SHR2', _float), ('AX', _float), ('T', _float), ('DOMAIN_ID', _int)],
    [0, 2, 3, 5, 6, 7, 8, 9],
    validator=_default_validator,
)


# beam

PunchTable('ELEMENT FORCES 2 BEAM REAL OUTPUT', 'BEAM', '/NASTRAN/RESULT/ELEMENTAL/FORCE', 'EID',
    [('EID', _int), ('GRID', _int, (11,)), ('DIST', _float, (11,)), ('M1', _float, (11,)), ('M2', _float, (11,)),
     ('SHR1', _float, (11,)), ('SHR2', _float, (11,)), ('AX', _float, (11,)), ('TT', _float, (11,)),
     ('WT', _float, (11,)), ('DOMAIN_ID', _int)],
    [0, slice(2, 101, 9), slice(3, 102, 9), slice(4, 103, 9), slice(5, 104, 9), slice(6, 105, 9), slice(7, 106, 9),
     (8, 107, 9), slice(9, 108, 9), slice(10, 109, 9)],
    validator=_default_validator,
)

# bush

PunchTable('ELEMENT FORCES 102 BUSH REAL OUTPUT', 'BUSH', '/NASTRAN/RESULT/ELEMENTAL/FORCE', 'EID',
    [('EID', _int), ('FX', _float), ('FY', _float), ('FZ'), ('MX', _float), ('MY', _float), ('MZ', _float),
     ('DOMAIN_ID', _int)],
    [0, 2, 3, 4, 5, 6, 7],
    validator=_default_validator,
)


# shell

shell_dtype = [('EID', _int), ('FX', _float), ('FY', _float), ('FXY', _float), ('MX', _float), ('MY', _float),
               ('MXY', _float), ('QX', _float), ('QY', _float)]

shell_indices = [0, 2, 3, 4, 5, 6, 7, 8, 9]

# quad4

PunchTable('ELEMENT FORCES 33 QUAD4 REAL OUTPUT MATERIAL', 'QUAD4', '/NASTRAN/RESULT/ELEMENTAL/FORCE', 'EID',
    shell_dtype,
    shell_indices,
    validator=_default_validator,
)


PunchTable('ELEMENT FORCES 33 QUAD4 REAL OUTPUT', 'QUAD4', '/NASTRAN/RESULT/ELEMENTAL/FORCE', 'EID',
    shell_dtype,
    shell_indices,
    validator=_default_validator,
)


# tria3

PunchTable('ELEMENT FORCES 74 TRIA3 REAL OUTPUT MATERIAL', 'TRIA3', '/NASTRAN/RESULT/ELEMENTAL/FORCE', 'EID',
    shell_dtype,
    shell_indices,
    validator=_default_validator,
)


PunchTable('ELEMENT FORCES 74 TRIA3 REAL OUTPUT', 'TRIA3', '/NASTRAN/RESULT/ELEMENTAL/FORCE', 'EID',
    shell_dtype,
    shell_indices,
    validator=_default_validator,
)


# quad4_cn

_dtype = [('EID', _int), ('TERM', _str4), ('GRID', _int, (5,)), ('FX', _float, (5,)), ('FY', _float, (5,)),
         ('FXY', _float, (5,)), ('MX', _float, (5,)), ('MY', _float, (5,)), ('QX', _float, (5,)), ('QY', _float, (5,)),
         ('DOMAIN_ID', _int)]

_indices = [0, 2, (DefinedValue(0), 12, 21, 30, 39), (4, 13, 22, 31, 40), (5, 14, 23, 32, 41), (6, 15, 24, 33, 42),
            (7, 16, 25, 34, 43), (8, 17, 26, 35, 44), (9, 18, 27, 36, 45), (10, 19, 28, 37, 46), (11, 20, 29, 38, 47)
]

PunchTable('ELEMENT FORCES 144 QUAD4C BILIN REAL OUTPUT', 'QUAD4_CN', '/NASTRAN/RESULT/ELEMENTAL/FORCE', 'EID',
    _dtype,
    _indices,
    validator=_default_validator,
)


PunchTable('ELEMENT FORCES 144 QUAD4C REAL OUTPUT', 'QUAD4_CN', '/NASTRAN/RESULT/ELEMENTAL/FORCE', 'EID',
    _dtype,
    _indices,
    validator=_default_validator,
)


# rod

PunchTable('ELEMENT FORCES 1 ROD REAL OUTPUT', 'ROD', '/NASTRAN/RESULT/ELEMENTAL/FORCE', 'EID',
    [('EID', _int), ('AX', _float), ('T', _float), ('DOMAIN_ID', _int)],
    [0, 2, 3],
    validator=_default_validator,
)


# shear

_dtype = [('EID', _int), ('F14', _float), ('F12', _float), ('F21', _float), ('F23', _float),
         ('F32', _float), ('F34', _float), ('F43', _float), ('F41', _float), ('K1', _float),
          ('SHR12', _float), ('K2', _float), ('SHR23', _float), ('K3', _float), ('SHR34', _float),
          ('K4', _float), ('SHR41', _float), ('DOMAIN_ID', _int)]

_indices = [0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]

PunchTable('ELEMENT FORCES 4 SHEAR MATERIAL REAL OUTPUT', 'SHEAR', '/NASTRAN/RESULT/ELEMENTAL/FORCE', 'EID',
    _dtype,
    _indices,
    validator=_default_validator,
)

PunchTable('ELEMENT FORCES 4 SHEAR REAL OUTPUT', 'SHEAR', '/NASTRAN/RESULT/ELEMENTAL/FORCE', 'EID',
    _dtype,
    _indices,
    validator=_default_validator,
)
