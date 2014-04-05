#!/usr/bin/python
# -*- coding: utf-8 -*-
# pylint: disable=R0904

""" Unit test suite for pymajka """

import unittest
import pymajka
import pexpect

class TestPyMajka(unittest.TestCase):
	""" Unit test suite for pymajka.Majka

		It requires an access to majka and two selected dictionaries. Testing attempts to cover
		all major situations when this class can be used. Including using several tokens in one
		"connection"
	"""
	MAJKA_PATH = "majka/majka"
	MAJKA_DICT = "majka/majka.w-lt"
	MAJKA_DICT_W = "majka/majka.w"
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
		self.assertEquals(u"pes:pes:k1gMnSc1:peso:k1gNnPc2", majka.get_raw(u"pes"))

	def test_tuple_lt_pes(self):
		""" Check if we obtain formatted tuples as expected for token "pes" """
		majka = pymajka.Majka("%s -f %s -p" % (self.MAJKA_PATH, self.MAJKA_DICT))
		result = majka.get_tuple(u"pes")
		self.assertEquals(2, len(result))
		self.assertEquals("peso", result[1][0])
		self.assertEquals("k1gNnPc2", result[1][1])

	def test_raw_dub(self):
		""" Check if we obtain same raw output as expected for token "dub" """
		majka = pymajka.Majka("%s -f %s -p" % (self.MAJKA_PATH, self.MAJKA_DICT))
		self.assertEquals("dub:dub:k1gInSc1:dub:k1gInSc4", majka.get_raw(u"dub"))

	def test_tuple_lt_dub(self):
		""" Check if we obtain formatted tuples as expected for token "pes" """
		majka = pymajka.Majka("%s -f %s -p" % (self.MAJKA_PATH, self.MAJKA_DICT))
		result = majka.get_tuple(u"dub")
		self.assertEquals(2, len(result))
		self.assertEquals("dub", result[0][0])
		self.assertEquals("k1gInSc1", result[0][1])

	def test_raw_xyz(self):
		""" Test raw results of analyzing token that does not exists in Czech database """
		majka = pymajka.Majka("%s -f %s -p" % (self.MAJKA_PATH, self.MAJKA_DICT))
		self.assertEquals("xyz", majka.get_raw(u"xyz"))

	def test_tuple_lt_xyz(self):
		""" Test formatted tuples of analyzing token that does not exists in Czech database """
		majka = pymajka.Majka("%s -f %s -p" % (self.MAJKA_PATH, self.MAJKA_DICT))
		result = majka.get_tuple(u"xyz")
		self.assertEquals(0, len(result))

	def test_tuple_w_pes(self):
		""" Check if we obtain formatted tuples as expected for token "pes" with different dictionary type"""
		majka = pymajka.Majka("%s -f %s -p" % (self.MAJKA_PATH, self.MAJKA_DICT_LW), "w")
		result = majka.get_tuple(u"pes")
		self.assertEquals(15, len(result))
		self.assertEquals("psa", result[1][0])

	def test_multiple(self):
		""" Test obtaining several analysis in one connection """
		majka = pymajka.Majka("%s -f %s -p" % (self.MAJKA_PATH, self.MAJKA_DICT))
		result = majka.get_tuple(u"xyz")
		self.assertEquals(0, len(result))
		result = majka.get_tuple(u"dub")
		self.assertEquals(2, len(result))
		self.assertEquals("k1gInSc1", result[0][1])

	def test_diacritics(self):
		""" Test non-ascii string - this should fail"""
		majka = pymajka.Majka("%s -f %s -p" % (self.MAJKA_PATH, self.MAJKA_DICT))
		with self.assertRaises(TypeError):
			result = majka.get_tuple("Ruská")

	def test_diacritics_unicode(self):
		""" Test non-ascii string """
		majka = pymajka.Majka("%s -f %s -p" % (self.MAJKA_PATH, self.MAJKA_DICT))
		result = majka.get_tuple(u"Ruská")

	def test_colon(self):
		""" Test colon which is normally a separator """
		majka = pymajka.Majka("%s -f %s -p" % (self.MAJKA_PATH, self.MAJKA_DICT))
		result = majka.get_tuple(u":")
		self.assertEquals(":", result[0][0])

	def test_unicode_lemma(self):
		""" Test lemma returned for unicode string """
		majka = pymajka.Majka("%s -f %s -p" % (self.MAJKA_PATH, self.MAJKA_DICT))
		result = majka.get_tuple(u"život")
		self.assertEquals(u"život", result[0][0])

	def test_preprocess_token(self):
		""" Test preprocessing of tokens e.g. unify i/y """
		class Ypsilon(pymajka.Majka):
			def preprocess(self, token):
				return token.replace(u"y", u"i").replace(u"Y", u"I").replace(u"ý", u"í").replace(u"Ý", u"Í")

		majka = Ypsilon("%s -f %s -p" % (self.MAJKA_PATH, self.MAJKA_DICT))
		self.assertEquals(u"pivo", majka.get_tuple(u"pyvo")[0][0])

	def test_capitalization(self):
		""" Test token which has first letter capital """
		class Capit(pymajka.Majka):
			def postprocess(self, token, results):
				# We expect that it is used only with "w" dictionaries
				if token == token.capitalize():
					final_result = []
					for result in results:
						final_result.append((result[0].capitalize(),))
					return final_result

				return results

		majka = Capit("%s -f %s -p" % (self.MAJKA_PATH, self.MAJKA_DICT_W), "w")
		result = majka.get_tuple(u"Žirafy")
		self.assertEquals(u"Žirafy", result[0][0])

	def test_uppercase(self):
		""" Test token which is written in uppercase only """
		class Capit(pymajka.Majka):
			def postprocess(self, token, results):
				# We expect that it is used only with "w" dictionaries
				if token == token.upper():
					final_result = []
					for result in results:
						final_result.append((result[0].upper(),))
					return final_result

				return results

		majka = Capit("%s -f %s -p" % (self.MAJKA_PATH, self.MAJKA_DICT_W), "w")
		result = majka.get_tuple(u"ŽIRAFY")
		self.assertEquals(u"ŽIRAFY", result[0][0])

	def test_colon_in_text(self):
		majka = pymajka.Majka("%s -f %s -p" % (self.MAJKA_PATH, self.MAJKA_DICT))
		result = majka.get_tuple(u"http://www.streettrutnov.cz")
		self.assertEquals(u"http://www.streettrutnov.cz", result[0][0])

	def test_colon_w(self):
		majka = pymajka.Majka("%s -f %s -p" % (self.MAJKA_PATH, self.MAJKA_DICT_W), "w")
		result = majka.get_tuple(u":")
		self.assertEquals(1, len(result))

	def test_colon_wl(self):
		majka = pymajka.Majka("%s -f %s -p" % (self.MAJKA_PATH, self.MAJKA_DICT))
		result = majka.get_tuple(u":")
		self.assertEquals(1, len(result))

	def test_colon_strange_char(self):
		majka = pymajka.Majka("%s -f %s -p" % (self.MAJKA_PATH, self.MAJKA_DICT))
		result = majka.get_tuple(u" ")


class TestPyMajkaRepair(unittest.TestCase):
	MAJKA_PATH = "majka/majka"
	MAJKA_Y_PATH = "majka/majka-marx-y"
	MAJKA_DICT_W = "majka/majka.w"

	def test_constructor(self):
		majka = pymajka.MajkaRepair("%s -f %s -p" % (self.MAJKA_PATH, self.MAJKA_DICT_W))

	def test_upper(self):
		majka = pymajka.MajkaRepair("%s -f %s -p" % (self.MAJKA_PATH, self.MAJKA_DICT_W))
		result = majka.get_tuple(u"ŽIRAFY")
		self.assertEquals(u"ŽIRAFY", result[0][0])

	def test_capitalization(self):
		majka = pymajka.MajkaRepair("%s -f %s -p" % (self.MAJKA_PATH, self.MAJKA_DICT_W))
		result = majka.get_tuple(u"Žirafy")
		self.assertEquals(u"Žirafy", result[0][0])

	def test_preprocess_token(self):
		""" Test preprocessing of tokens e.g. unify i/y """
		class Ypsilon(pymajka.MajkaRepair):
			def preprocess(self, token):
				return token.replace(u"y", u"i").replace(u"Y", u"I").replace(u"ý", u"í").replace(u"Ý", u"Í")

		majka = Ypsilon("%s -f %s -p" % (self.MAJKA_Y_PATH, self.MAJKA_DICT_W))
		self.assertEquals(u"Žirafy", majka.get_tuple(u"Žirafy")[0][0])
		self.assertEquals(u"Žirafy", majka.get_tuple(u"Žirafi")[0][0])

if __name__ == '__main__':
	unittest.main()
