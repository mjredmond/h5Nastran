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


def format_float_data(card_data, card_len=16):
    if not isinstance(card_data, float):
        card_data = float(card_data)

    if card_data > 0.:
        prefix = ''
    else:
        prefix = '-'
        card_len -= 1

    card_data = abs(card_data)

    card_txt = str(card_data)

    # while card_txt[0] == '0':
    #     card_txt = card_txt[1:]
    #
    # while card_txt[-1] == '0':
    #     card_txt = card_txt[:-1]

    card_txt = card_txt.strip(' 0')

    if len(card_txt) <= card_len:
        if prefix != '':
            fmt = "%" + "%ds" % (card_len+1)
        else:
            fmt = "%" + "%ds" % card_len

        result = prefix + card_txt.strip()

        if result == '.' or result == '-.':
            result = '.0'

        return fmt % result

    from math import log10
    exponent = int(log10(card_data))

    if exponent > 0.:
        exponent = "+" + str(exponent)
    else:
        exponent = str(exponent)

    remaining_width = card_len - len(exponent)

    tmp = card_txt.split('.')
    no_decimals = tmp[0] + tmp[1]

    if card_data >= 1.:
        before_decimal = no_decimals[0] + '.'
        after_decimal = no_decimals[1:]
    else:
        before_decimal = '.'
        after_decimal = no_decimals

    remaining_width -= len(before_decimal)

    after_decimal = after_decimal[:remaining_width]

    return prefix + before_decimal + after_decimal + exponent


def format_data(card_data, card_len=16):
    if isinstance(card_data, str):
        fmt = "%" + "%ds" % card_len
        return fmt % card_data.strip()
    elif isinstance(card_data, int):
        fmt = "%" + "%dd" % card_len
        return fmt % card_data
    elif isinstance(card_data, float):
        return format_float_data(card_data, card_len)
    elif card_data is None:
        return ' '*card_len
    else:
        print(card_data)
        raise Exception


def expand_list(text_list):
    parts = text_list.split(' ')

    result = []

    for part in parts:
        if part.replace(' ', '') == '':
            continue

        parts_ = part.split(':')
        try:
            first = int(parts_[0])
        except IndexError:
            first = int(parts_)
        except ValueError:
            print(text_list)
            print(part)
            print(parts_)
            raise

        try:
            last = int(parts_[1])
        except IndexError:
            last = first

        try:
            offset = int(parts_[2])
        except IndexError:
            offset = 1

        for id_ in range(first, last + offset, offset):
            result.append(id_)

    return result
