import unittest
import sys
import json
from core.pop import Pop
from libs.core_utils import IPA, export_to_file


class Pop_functions_in_isolation(unittest.TestCase):

	def test_import_export(self):
		pop1 = Pop("here", "there")
		json1 = pop1.serialize_to_json()
		pop2 = Pop("over there", "way over there")
		pop2.import_from_json(json1)
		self.assertEqual(pop1, pop2)
		pop3 = Pop("hin", "her", json=json1)
		self.assertEqual(pop1, pop3)


if __name__ == '__main__':
    unittest.main()