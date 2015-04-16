""" Python interface to morphological analyser majka """
import ctypes

STDLIB = "majka/libmajka.so"

# Available flags
#	Add diacritics can be used also for other library specific transformation e.g i/y
#
ADD_DIACRITICS = 1
IGNORE_CASE = 2

class Majka(object):
	""" Python interface to morphological analyser majka

		This class provides easy access to the morphological analyser. It is based on the command-line
		interface so it should be rock stable. In order to start using this class you have to provide path
		to binary of majka, dictionary path and information about used dictionary which is used to properly
		group morphological data together.

		During development, I was following a test-driven development what should help you to understand
		basic usage. Just take a look at unittest in pymajka_test.py
	"""
	def __init__(self, dictionary, dict_type="lt", flag=0, library=STDLIB):
		self.libmajka = ctypes.CDLL(library)
		self.libmajka.fsa_find_first.restype = ctypes.c_char_p
		self.libmajka.fsa_find_next.restype = ctypes.c_char_p
		self.majka = self.libmajka.fsa_new(dictionary)

		self.flag = flag
		self.dict_type = dict_type

	def preprocess(self, token):
		""" Preprocess token before it is processed by get_tuple()
			Input/output is always unicode"""

		return token

	def postprocess(self, token, tuples):
		""" Postprocess results to obtain a preffered form e.g. capitalization """
		del token
		return tuples

	def get_raw(self, token):
		""" Get raw output from majka """
		if not isinstance(token, unicode):
			raise TypeError("Only unicode strings are accepted by Majka")

		results = []

		response = self.libmajka.fsa_find_first(self.majka, token.encode("utf-8"), self.flag)
		while not response == "":
			results.append(response)
			response = self.libmajka.fsa_find_next(self.majka)

		return results

	def get_tuple(self, token):
		""" Get tuples from majka output formated into pairs/triplets/... according to dict_type """
		if not isinstance(token, unicode):
			raise TypeError("Only unicode strings are accepted by Majka")

		processed_token = self.preprocess(token)

		out = []
		majka_output = [unicode(x.decode("utf-8")) for x in self.get_raw(processed_token)]
		if len(majka_output) > 0:
			for entry in majka_output:
				out.append(entry.split(":"))
		else:
			out = []
		return self.postprocess(token, out)

class MajkaRepair(Majka):
	""" Extension of Majka which should be used for situation when you have to repair word

		This class targets a real-world usage, so it is able to handle capitalization/uppercase for
		common situation. Usually you wish to create child of this class which will add a unifying
		preprocessing e.g. remove diacritics / merge i/y together
	"""

	def __init__(self, dictionary, library=STDLIB):
		Majka.__init__(self, dictionary, dict_type="w", library=library, flag=1)

	def postprocess(self, token, results):
		if token == token.upper():
			return [(r[0].upper(),) for r in results]
		elif token == token.capitalize():
			return [(r[0].capitalize(),) for r in results]
		else:
			return results
