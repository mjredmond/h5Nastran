from __future__ import print_function, absolute_import
from six import iteritems, itervalues
from six.moves import range


from collections import OrderedDict
import xml.etree.ElementTree as ET

import numpy as np



typedefs = {
    'integer': '<i8',
    'double': '<f8'
}


class Field(object):
    def __init__(self, name, data_type, shape, description):
        self.name = name
        self.data_type = data_type
        self.shape = shape
        self.description = description

    def __repr__(self):
        return self.name, self.data_type, self.shape, self.description

    def to_dtype(self):
        data_type = typedefs.get(self.data_type, self.data_type)
        try:
            data_type = data_type.to_dtype()
        except AttributeError:
            pass

        return self.name, data_type, self.shape


class Typedef(object):
    def __init__(self, name, fields):
        self.name = name
        self.fields = fields

    def __repr__(self):
        data = [self.name]
        data.append([field.__repr__() for field in self.fields])
        return str(data)

    def to_dtype(self):
        dtypes = []

        for field in self.fields:
            dtypes.append(field.to_dtype())

        return np.dtype(dtypes)


class Group(object):
    def __init__(self, name, children):
        self.parent = None
        self.name = name
        self.children = children

        self.set_parent()

    def set_parent(self):
        for child in itervalues(self.children):
            child.parent = self
            child.set_parent()

    def path(self):
        try:
            parent_path = self.parent.path()
        except AttributeError:
            parent_path = []

        return parent_path + [self.name]

    def __getitem__(self, item):
        return self.children[item]

    def __repr__(self):
        return self.children.__repr__()

    def is_multitable(self):
        return 'IDENTITY' in self.children


class Dataset(Typedef):
    def __init__(self, name, fields):
        super(Dataset, self).__init__(name, fields)
        self.parent = None

    def set_parent(self):
        pass

    def path(self):
        try:
            parent_path = self.parent.path()
        except AttributeError:
            parent_path = []

        return parent_path + [self.name]


def get_field(data):
    items = OrderedDict(data.items())

    name = items['name']
    data_type = items['type']
    size = items.get('size', None)
    description = items.get('description', '')

    if size is None:
        shape = ()
    else:
        shape = (int(size),)

    if data_type == 'character':
        data_type = 'S%d' % int(size)
        shape = ()

    return Field(name, data_type, shape, description)


def get_typedef(data):
    items = OrderedDict(data.items())

    name = items['name']
    fields = []

    children = data.getchildren()

    for child in children:
        fields.append(get_field(child))

    return Typedef(name, fields)


def get_dataset(data):
    items = OrderedDict(data.items())

    name = items['name']
    fields = []

    children = data.getchildren()

    for child in children:
        fields.append(get_field(child))

    return Dataset(name, fields)


def get_typedefs(data):
    children = data.getchildren()

    for child in children:
        typedef = get_typedef(child)
        typedefs[typedef.name] = typedef

    return typedefs


def get_group(parent):
    items = OrderedDict(parent.items())
    name = items.get('name', '')

    group_children = OrderedDict()

    children = parent.getchildren()

    for child in children:
        tag = child.tag
        if tag == 'group':
            child = get_group(child)
        elif tag == 'dataset':
            child = get_dataset(child)

        group_children[child.name] = child

    return Group(name, group_children)



tree = ET.parse('DataType.xml')
root = tree.getroot()


get_typedefs(root.getchildren()[0])

print(typedefs)

groups = get_group(root.getchildren()[1])

group = groups['NASTRAN']['INPUT']['PROPERTY']['PBARL']

print(group.path())

print(group.children)

print(group['IDENTITY'].to_dtype())

