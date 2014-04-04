""" Python interface to morphological analyser majka """
import pexpect
import sys
import logging

class Majka:
	""" Python interface to morphological analyser majka

		This class provides easy access to the morphological analyser. It is based on the command-line
		interface so it should be rock stable. In order to start using this class you have to provide path
		to binary of majka, dictionary path and information about used dictionary which is used to properly
		group morphological data together.

		During development, I was following a test-driven development what should help you to understand
		basic usage. Just take a look at unittest in pymajka_test.py
	"""
	def __init__(self, command, dict_type = "lt"):
		self.process = None
		self.dict_type = dict_type
		self.timeout = 1

		self.conn = pexpect.spawn(command)

	def preprocess(self, token):
		""" Preprocess token before it is processed by get_tuple()

			Input/output is always unicode"""
		return token

	def postprocess(self, token, tuples):
		""" Postprocess results to obtain a preffered form e.g. capitalization """

		return tuples

	def get_raw(self, token):
		""" Get raw output from majka """
		if not isinstance(token, unicode):
			raise TypeError("Only unicode strings are accepted by Majka")

		self.conn.send(token.encode("utf-8") + "\n")
		self.conn.expect("\n", self.timeout)
		self.conn.expect("\n", self.timeout)
		output = self.conn.before.rstrip()

		return output

	def get_tuple(self, token):
		""" Get tuples from majka output formated into pairs/triplets/... according to dict_type """
		if not isinstance(token, unicode):
			raise TypeError("Only unicode strings are accepted by Majka")

		processed_token = self.preprocess(token)
		elements = self.get_raw(processed_token).split(":")
		elements = [ unicode(x.decode("utf-8")) for x in elements ]

		if processed_token == ":":
			elements = [":", ":", ":"]
		elif processed_token != elements[0]:
			logging.error("majka returned invalid output for token >%s< vs >%s<" % (processed_token, elements[0]))
			sys.exit(1)

		if len(self.dict_type) == 1:
			pairs = zip(elements[1::1])
		elif len(self.dict_type) == 2:
			pairs = zip(elements[1::2], elements[2::2])
		else:
			logging.error("we do not support more than pairs on output")
			sys.exit(2)

		return self.postprocess(token, pairs)

class MajkaRepair(Majka):
	""" Extension of Majka which should be used for situation when you have to repair word

		This class targets a real-world usage, so it is able to handle capitalization/uppercase for
		common situation. Usually you wish to create child of this class which will add a unifying
		preprocessing e.g. remove diacritics / merge i/y together
	"""

	def __init__ (self, command):
		Majka.__init__(self, command, "w")

	def postprocess(self, token, results):
		if token == token.upper():
			return map(lambda r: (r[0].upper(),), results)
		elif token == token.capitalize():
			return map(lambda r: (r[0].capitalize(),), results)
		else:
			return results
