#!/usr/bin/python
# -*- coding: utf-8 -*-
# pylint: disable=R0904

""" Unit test suite for pymajka """

import unittest
import pymajka
import pexpect

class TestPyMajka(unittest.TestCase):
	""" Unit test suite for pymajka

		It requires an access to majka and two selected dictionaries. Testing attempts to cover
		all major situations when this class can be used. Including using several tokens in one
		"connection"
	"""
	MAJKA_PATH = "majka/majka"
	MAJKA_DICT = "majka/majka.w-lt"
	MAJKA_DICT_LW = "majka/majka.l-w"

	def test_constructor_basic(self):
		""" Test basic constructor with default dictionary type """
		pymajka.Majka("%s -f %s -p" % (self.MAJKA_PATH, self.MAJKA_DICT))

	def test_constructor_wl(self):
		""" Test basic constructor with given dictionary type """
		pymajka.Majka("%s -f %s -p" % (self.MAJKA_PATH, self.MAJKA_DICT), "wl")

	def test_run_noexec(self):
		""" Test attempt to run file that exists but is not executable """
		with self.assertRaises(pexpect.ExceptionPexpect):
			pymajka.Majka(["/etc/passwd"])

	def test_run_noexist(self):
		""" Test attempt to run file that does not exist """
		with self.assertRaises(pexpect.ExceptionPexpect):
			pymajka.Majka(["/no/such/file"])

	def test_raw_pes(self):
		""" Check if we obtain same raw output as expected for token "pes" """
		majka = pymajka.Majka("%s -f %s -p" % (self.MAJKA_PATH, self.MAJKA_DICT))
		self.assertEquals("pes:pes:k1gMnSc1:peso:k1gNnPc2", majka.get_raw("pes"))

	def test_tuple_lt_pes(self):
		""" Check if we obtain formatted tuples as expected for token "pes" """
		majka = pymajka.Majka("%s -f %s -p" % (self.MAJKA_PATH, self.MAJKA_DICT))
		result = majka.get_tuple("pes")
		self.assertEquals(2, len(result))
		self.assertEquals("peso", result[1][0])
		self.assertEquals("k1gNnPc2", result[1][1])

	def test_raw_dub(self):
		""" Check if we obtain same raw output as expected for token "dub" """
		majka = pymajka.Majka("%s -f %s -p" % (self.MAJKA_PATH, self.MAJKA_DICT))
		self.assertEquals("dub:dub:k1gInSc1:dub:k1gInSc4", majka.get_raw("dub"))

	def test_tuple_lt_dub(self):
		""" Check if we obtain formatted tuples as expected for token "pes" """
		majka = pymajka.Majka("%s -f %s -p" % (self.MAJKA_PATH, self.MAJKA_DICT))
		result = majka.get_tuple("dub")
		self.assertEquals(2, len(result))
		self.assertEquals("dub", result[0][0])
		self.assertEquals("k1gInSc1", result[0][1])

	def test_raw_xyz(self):
		""" Test raw results of analyzing token that does not exists in Czech database """
		majka = pymajka.Majka("%s -f %s -p" % (self.MAJKA_PATH, self.MAJKA_DICT))
		self.assertEquals("xyz", majka.get_raw("xyz"))

	def test_tuple_lt_xyz(self):
		""" Test formatted tuples of analyzing token that does not exists in Czech database """
		majka = pymajka.Majka("%s -f %s -p" % (self.MAJKA_PATH, self.MAJKA_DICT))
		result = majka.get_tuple("xyz")
		self.assertEquals(0, len(result))

	def test_tuple_w_pes(self):
		""" Check if we obtain formatted tuples as expected for token "pes" with different dictionary type"""
		majka = pymajka.Majka("%s -f %s -p" % (self.MAJKA_PATH, self.MAJKA_DICT_LW), "w")
		result = majka.get_tuple("pes")
		self.assertEquals(15, len(result))
		self.assertEquals("psa", result[1][0])

	def test_multiple(self):
		""" Test obtaining several analysis in one connection """
		majka = pymajka.Majka("%s -f %s -p" % (self.MAJKA_PATH, self.MAJKA_DICT))
		result = majka.get_tuple("xyz")
		self.assertEquals(0, len(result))
		result = majka.get_tuple("dub")
		self.assertEquals(2, len(result))
		self.assertEquals("k1gInSc1", result[0][1])

	def test_diacritics(self):
		""" Test non-ascii string """
		majka = pymajka.Majka("%s -f %s -p" % (self.MAJKA_PATH, self.MAJKA_DICT))
		result = majka.get_tuple("Ruská")

	def test_diacritics_unicode(self):
		""" Test non-ascii string """
		majka = pymajka.Majka("%s -f %s -p" % (self.MAJKA_PATH, self.MAJKA_DICT))
		result = majka.get_tuple(u"Ruská")

	def test_colon(self):
		""" Test colon which is normally a separator """
		majka = pymajka.Majka("%s -f %s -p" % (self.MAJKA_PATH, self.MAJKA_DICT))
		result = majka.get_tuple(":")
		self.assertEquals(":", result[0][0])

if __name__ == '__main__':
	unittest.main()
