pymajka
=======

pymajka - python interface to morphological analyser majka

Plain usage:

import pymajka

majka = pymajka.Majka("majka/majka.l-wt", library="majka/libmajka.so")

result = majka.get_tuple(u"pes")

Add diacritics variant:

import majka

majka = pymajka.Majka("majka/majka.l-wt", library="majka/libmajka.so", flag=pymajka.ADD_DIACRITICS)

result = majka.get_tuple(u"zirafa")
