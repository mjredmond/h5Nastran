from __future__ import print_function, absolute_import
from six import iteritems, iterkeys, itervalues
from six.moves import range

from _file_reader import FileReader

import re


filename = r'../files/static_solid_shell_bar_xyz.f06'

f = FileReader(filename)

while True:
    line = f.next_line()

    if line is None:
        break

    print(re.split(b' +', line))

