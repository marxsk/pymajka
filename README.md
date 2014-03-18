pymajka
=======

pymajka - python interface to morphological analyser majka

Usage:

import pymajka

majka = pymajka.Majka("%s -f %s -p" % (self.MAJKA_PATH, self.MAJKA_DICT))
result = majka.get_tuple("pes")
