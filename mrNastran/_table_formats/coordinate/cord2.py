"""
Copyright (C) Michael James Redmond, Jr - All Rights Reserved
Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Michael James Redmond, Jr.
"""
from __future__ import print_function, absolute_import
from six import iteritems, itervalues
from six.moves import range

from tables import IsDescription, Int64Col, Float64Col, StringCol
import tables

from ..abstract_table import AbstractTable
from .._main import register_table


def _register(card_name):

    def inner(cls):
        class _Tmp(cls):
            group = '/NASTRAN/INPUT/COORDINATE'
            table_id = card_name
            table_path = '%s/%s' % (group, table_id)

        register_table(card_name)(_Tmp)

        return cls

    return inner


@_register('CORD2C')
@_register('CORD2R')
@_register('CORD2RX')
@_register('CORD2S')
class CORD2(AbstractTable):
    group = '/NASTRAN/INPUT/COORDINATE'
    table_id = ''
    table_path = ''

    class Format(IsDescription):
        CID = Int64Col(pos=1)
        RID = Int64Col(pos=2)
        A = Float64Col(shape=3, pos=3)
        B = Float64Col(shape=3, pos=4)
        C = Float64Col(shape=3, pos=5)
        DOMAIN_ID = Int64Col(pos=6)

    @classmethod
    def _write_data(cls, h5f, table_data, h5table):
        table_row = h5table.row

        domain = cls.domain_count

        ids = sorted(table_data.keys())

        for _id in ids:

            # TODO: what to do about multiple definitions?
            data_i = table_data[_id][0].data
            data_i_get = data_i.get

            table_row['CID'] = data_i[1]
            table_row['RID'] = data_i_get(2, 0)
            table_row['A'] = data_i[3:6]
            table_row['B'] = data_i[6:9]
            table_row['C'] = data_i[9:12]
            table_row['DOMAIN_ID'] = domain

            table_row.append()

        h5f.flush()
