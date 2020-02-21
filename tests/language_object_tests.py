import unittest
import sys
from core.language import Language
from libs.core_utils import IPA


class Language_functions_in_isolation(unittest.TestCase):

    def test_phonetic_inv(self):
        test_language = Language("Testlish", None)
        pi = test_language.create_phonetic_inventory(None)
        for p in pi:
            print(p)
            print(IPA[p])
        self.assertTrue(len(pi) == 36 or len(pi) == 35)


if __name__ == '__main__':
    unittest.main()