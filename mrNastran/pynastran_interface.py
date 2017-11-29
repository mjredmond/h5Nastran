"""
Interfaces to pynastran bdf file.  Returns a dict of all card objects where the key is the card name.
"""

from six import iteritems


def get_bdf_cards(bdf):
    """

    :type bdf: pyNastran.bdf.bdf.BDF
    :return:
    """

    cards = {}

    def _add_cards_from_dict(obj):
        for key, value in iteritems(obj):
            if isinstance(value, (list, tuple)):
                card_type = value[0].type

                try:
                    cards[card_type]
                except KeyError:
                    cards[card_type] = {}

                cards[card_type][key] = [_.repr_fields() for _ in value]
            else:
                card_type = value.type

                try:
                    cards[card_type]
                except KeyError:
                    cards[card_type] = {}

                cards[card_type][key] = value.repr_fields()

    def _add_cards_from_list(obj):
        for value in obj:
            if isinstance(value, (list, tuple)):
                card_type = value[0].type

                try:
                    data = cards[card_type]
                except KeyError:
                    data = cards[card_type] = []

                for _ in value:
                    data.append(_.repr_fields())

            else:
                card_type = value.type

                try:
                    cards[card_type].append(value.repr_fields())
                except KeyError:
                    cards[card_type] = [value.repr_fields()]

    attrs = [
        'nodes', 'coords', 'elements', 'properties', 'rigid_elements', 'plotels', 'masses', 'properties_mass',
        'materials', 'thermal_materials', 'MATS1', 'MATS3', 'MATS8', 'MATT1', 'MATT2', 'MATT3', 'MATT4', 'MATT5', 'MATT8', 'MATT9', 'creep_materials', 'hyperelastic_materials',
        'load_combinations', 'loads', 'tics', 'dloads', 'dload_entries',
        'nlpcis', 'nlparms', 'rotors', 'tsteps', 'tstepnls', 'transfer_functions', 'delays',
        'aeros', 'caeros', 'paeros', 'splines',
        'aecomps', 'aefacts', 'aelinks', 'aeparams', 'aesurf', 'aesurfs', 'aestats', 'trims', 'divergs', 'csschds', 'mkaeros', 'monitor_points',
        'aero', 'flfacts', 'flutters', 'gusts',
        'bcs', 'phbdys', 'convection_properties', 'tempds',
        'bcrparas', 'bctadds', 'bctparas', 'bctsets', 'bsurf', 'bsurfs',
        'suport1', 'suport', 'se_suport',
        'spcadds', 'spcs', 'mpcadds', 'mpcs',
        'dareas', 'dphases', 'pbusht', 'pdampt', 'pelast', 'frequencies',
        'dmis', 'dmigs', 'dmijs', 'dmijis', 'dmiks',
        'sets', 'usets', 'asets', 'bsets', 'csets', 'qsets', 'se_sets', 'se_usets', 'se_bsets', 'se_csets', 'se_qsets',
        'tables', 'tables_d', 'tables_m', 'random_tables', 'tables_sdamping',
        'methods', 'cMethods',
        'dconadds', 'dconstrs', 'desvars', 'ddvals', 'dlinks', 'dresps', 'dtable', 'doptprm', 'dequations', 'dvprels', 'dvmrels', 'dvcrels', 'dscreen', 'dvgrids',
    ]

    for attr in attrs:
        _attr = getattr(bdf, attr)
        if attr is None:
            continue
        if isinstance(_attr, dict):
            _add_cards_from_dict(_attr)
        elif isinstance(_attr, list):
            _add_cards_from_list(_attr)

    return cards


if __name__ == '__main__':
    from pyNastran.bdf.bdf import BDF

    bdf = BDF()
    bdf.read_bdf(r'file.bdf')

    # cards = get_bdf_cards(bdf)

    # print(cards['CQUAD4'])

    print(bdf.properties[200007].repr_fields())


