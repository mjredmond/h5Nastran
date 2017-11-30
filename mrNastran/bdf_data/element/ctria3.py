from __future__ import print_function, absolute_import
from six import iteritems, itervalues
from six.moves import range

from tables import IsDescription, Int64Col, Float64Col, StringCol
import tables

from .._abstract_table import AbstractTable
from ._element import ElementCard

import numpy as np


class Ctria3Table(AbstractTable):
    group = '/NASTRAN/INPUT/ELEMENT'
    table_id = 'CTRIA3'
    table_path = '%s/%s' % (group, table_id)

    dtype = np.dtype([
        ('EID', np.int64),
        ('PID', np.int64),
        ('GRID', np.int64, (3,)),
        ('THETA', np.float64),
        ('MCID', np.int64),
        ('ZOFFS', np.float64),
        ('TFLAG', np.int64),
        ('Ti', np.float64, (3,)),
        ('DOMAIN_ID', np.int64)
    ])

    Format = tables.descr_from_dtype(dtype)[0]

    @classmethod
    def _write_data(cls, h5f, cards, h5table):
        table_row = h5table.row

        domain = cls.domain_count

        eids = sorted(cards.keys())

        for eid in eids:
            data = cards[eid]
            """:type data: pyNastran.bdf.cards.elements.shell.CQUAD4"""

            table_row['EID'] = data.eid
            table_row['PID'] = data.pid
            table_row['GRID'] = data.node_ids

            if isinstance(data.theta_mcid, int):
                mcid = data.theta_mcid
                theta = np.nan
            else:
                mcid = 0
                theta = data.theta_mcid

            table_row['THETA'] = theta
            table_row['MCID'] = mcid

            table_row['ZOFFS'] = data.zoffset
            table_row['TFLAG'] = data.tflag

            table_row['Ti'] = [data.T1, data.T2, data.T3]

            table_row['DOMAIN_ID'] = domain

            table_row.append()

        h5f.flush()


class CTRIA3(ElementCard):
    table_reader = Ctria3Table
    dtype = table_reader.dtype
