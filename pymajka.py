""" Python interface to morphological analyser majka """
import pexpect
import sys

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

	def get_raw(self, token):
		""" Get raw output from majka """
		self.conn.send(token + "\n")
		self.conn.expect("\n", self.timeout)
		self.conn.expect("\n", self.timeout)
		output = self.conn.before.rstrip()

		return output

	def get_tuple(self, token):
		""" Get tuples from majka output formated into pairs/triplets/... according to dict_type """
		elements = self.get_raw(token).split(":")

		if isinstance(token, unicode):
			elements[0] = unicode(elements[0].decode("utf-8"))

		if token == ":":
			elements = [":", ":", ":"]
		elif token != elements[0]:
			print >> sys.stderr, "majka returned invalid output for token >%s< vs >%s<" % (token, elements[0])
			sys.exit(1)

		if len(self.dict_type) == 1:
			pairs = zip(elements[1::1])
		elif len(self.dict_type) == 2:
			pairs = zip(elements[1::2], elements[2::2])
		else:
			print >> sys.stderr, "we do not support more than pairs on output"
			sys.exit(2)

		return pairs
