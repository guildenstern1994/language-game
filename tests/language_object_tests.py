import unittest
import sys
sys.path.insert(0, '/the/folder/path/name-folder/')
from core.language import Language


class Language_functions_in_isolation(unittest.TestCase):

	def test_phonetic_inv():
		test_language = Language("Testlish", None)
		pi = test_language.create_phonetic_inventory()
		for p in pi:
			print(p)
		self.assertEqual(len(pi, 36))