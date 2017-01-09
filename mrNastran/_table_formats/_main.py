"""
Copyright (C) Michael James Redmond, Jr - All Rights Reserved
Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Michael James Redmond, Jr.
"""
from __future__ import print_function, absolute_import
from six import iteritems, itervalues
from six.moves import range


data_tables = {}


def register_table(table_name):
    def inner(cls):
        class _Copy(cls):
            results_type = table_name

        data_tables[table_name] = _Copy

        return cls
    return inner


def get_table(table_name):
    return data_tables.get(table_name, None)
