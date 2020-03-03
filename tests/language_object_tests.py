import unittest
import sys
from core.language import Language, CharacterSet
from libs.core_utils import IPA


class Language_functions_in_isolation(unittest.TestCase):

    def test_phonetic_inv(self):
        test_language = Language("Testlish", None)
        pi = test_language.create_phonetic_inventory(None)
        self.assertTrue(506 in pi)
        self.assertEqual(type(pi), list)
        for item in pi:
            # print(type(item))
            self.assertTrue(type(item) is int)

    def test_create_phonetic_probs(self):
        test_language = Language("Testlish", None)
        pp = test_language.create_phonetic_probs(None)
        self.assertTrue('^' in pp.keys())
        self.assertTrue(type(pp) is dict)
        for key in pp.keys():
            self.assertTrue(type(key) is int or key == '^')
            self.assertTrue(type(pp[key]) is dict)
            for subkey in pp[key].keys():
                self.assertTrue(type(subkey) is int)
                self.assertTrue(type(pp[key][subkey]) is float)

    def test_create_word_order(self):
        test_language = Language("Testlish", None)
        wo = test_language.create_word_order(None)
        # print(wo)
        self.assertTrue(type(wo) is str)

    def test_create_script(self):
        test_language = Language("Testlish", None)
        sc = test_language.create_script(None, "no_script")
        self.assertEqual(test_language.script_type, "no_script")
        self.assertEqual(sc, [])
        sc2 = test_language.create_script(None, None)
        self.assertTrue(type(test_language.script_type) is str)
        self.assertTrue(test_language.script_type != "no_script")
        size = 20
        sc3 = test_language.create_script(None, None, size=size)
        self.assertTrue(len(sc3) == 20)
        self.assertTrue(type(sc3) is list)
        for element in sc3:
            self.assertTrue(type(element) is str)

    def test_choose_character_set(self):
        test_language = Language("Testlish", None)
        cs = test_language.choose_character_set()
        self.assertTrue(type(cs) is CharacterSet)
        self.assertTrue(type(cs.chars) is list)
        for c in cs.chars:
            self.assertTrue(type(c) is str)
        self.assertTrue(type(cs.type) is str)


if __name__ == '__main__':
    unittest.main()