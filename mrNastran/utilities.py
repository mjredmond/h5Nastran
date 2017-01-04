"""
Copyright (C) Michael James Redmond, Jr - All Rights Reserved
Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Michael James Redmond, Jr.
"""
from __future__ import print_function, absolute_import
from six import iteritems, itervalues
from six.moves import range


from math import log10
import re


def convert_field(value):
    """Converts a BDF field to double or integer if it is a string and returns the value.

    """

    if isinstance(value, float) or isinstance(value, int):
        return value

    assert isinstance(value, str)

    value = value.strip()
    try:
        if not value:
            # Empty
            return None
        elif value[0].isalpha():
            # Character
            return value
        elif '.' in value:
            # Real
            i = value.rfind('+')
            if i > 0 and value[i - 1] != 'E':
                value = value[:i] + 'E' + value[i:]
            i = value.rfind('-')
            if i > 0 and value[i - 1] != 'E':
                value = value[:i] + 'E' + value[i:]
            return float(value)
        else:
            # Integer
            return int(value)
    except ValueError:
        raise ValueError('field is not a string, double, or integer!')


def format_double(value, field_width):
    """Formats a double field.  If the value is too large for the field, it is converted to scientific notation.

    """

    str_value = str(value)
    if len(str_value) > field_width:
        exponent = int(log10(abs(value)))
        small_value = value/10**exponent

        exponent_str = str(exponent)
        if exponent > 0:
            exponent_str = '+' + exponent_str

        what_is_left = field_width - len(exponent_str)

        option = 0

        if small_value >= 1.:
            decimals = what_is_left - 2
        elif small_value >= 0.:
            decimals = what_is_left - 1
            option = 1
        elif small_value <= -1.:
            decimals = what_is_left - 3
        elif small_value > -1.:
            decimals = what_is_left - 2
            option = 2

        # noinspection PyUnboundLocalVariable
        if decimals < 0:
            decimals = 0

        _format = r'%' + str(what_is_left) + r'.' + str(decimals) + 'f'

        str_value = _format % small_value + exponent_str

        if option == 1:
            str_value = str_value[1:]
        elif option == 2:
            str_value = str_value.replace('-0.', '-.')

    return str_value


def chunk_string(in_str, width):
    return re.findall('.{%d}' % width, in_str)