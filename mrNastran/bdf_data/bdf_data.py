from __future__ import print_function, absolute_import
from six import iteritems, iterkeys, itervalues
from six.moves import range

import tables as tb

from .node import Node
from .constraint import Constraint
from .coordinate import Cord
from .element import Element
from .load import Load
from .material import Material
from .property import Property
from .rigid_element import RigidElement


class BDFData(object):
    def __init__(self):
        self.constraint = Constraint(self)
        self.cord = Cord(self)
        self.element = Element(self)
        self.load = Load(self)
        self.material = Material(self)
        self.node = Node(self)
        self.property = Property(self)
        self.rigid_element = RigidElement(self)

    def read_h5(self, h5f):
        if isinstance(h5f, str):
            h5f = tb.open_file(h5f, 'r')

        for attr in itervalues(self.__dict__):
            # TODO: assert instance, need to subclass
            attr.read_h5(h5f)

        # self.grid.read_h5(h5f)
        # self.cord.read_h5(h5f)
        # self.element.read_h5(h5f)
        # self.load.read_h5(h5f)
        # self.material.read_h5(h5f)
        # self.property.read_h5(h5f)
