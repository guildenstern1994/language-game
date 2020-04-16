import unittest
import sys
import json
from core.language import Language, CharacterSet
from libs.core_utils import IPA, export_to_file


class Language_functions_in_isolation(unittest.TestCase):

    def test_phonetic_inv(self):
        test_language = Language( None)
        pi = test_language.create_phonetic_inventory(None)
        self.assertTrue(506 in pi)
        self.assertEqual(type(pi), list)
        for item in pi:
            # print(type(item))
            self.assertTrue(type(item) is int)

    def test_create_phonetic_probs(self):
        test_language = Language(None)
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
        test_language = Language( None)
        wo = test_language.create_word_order(None)
        # print(wo)
        self.assertTrue(type(wo) is str)

    def test_create_script(self):
        test_language = Language( None)
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
        test_language = Language( None)
        cs = test_language.choose_character_set()
        self.assertTrue(type(cs) is CharacterSet)
        self.assertTrue(type(cs.chars) is list)
        for c in cs.chars:
            self.assertTrue(type(c) is str)
        self.assertTrue(type(cs.type) is str)

    def test_map_phonemes_to_graphemes(self):
        test_language = Language( None, script_type="no_script")
        test_language.map_phonemes_to_graphemes()
        self.assertTrue(test_language.phoneme_to_grapheme_map == {})
        lang2 = Language( None, script_type="alphabet")
        lang2.map_phonemes_to_graphemes()
        for key in lang2.phoneme_to_grapheme_map.keys():
            self.assertTrue(type(key) is int)
            self.assertTrue(type(lang2.phoneme_to_grapheme_map[key]) is dict)
            cur_sum = 0
            # print(IPA[key])
            # print("Key2    value")
            for key2 in lang2.phoneme_to_grapheme_map[key].keys():
                # print(key2 + "    " + str(lang2.phoneme_to_grapheme_map[key][key2]))
                self.assertTrue(type(key2) is str)
                self.assertTrue(type(lang2.phoneme_to_grapheme_map[key][key2] is float))
                cur_sum += lang2.phoneme_to_grapheme_map[key][key2]
            # print(cur_sum)
            self.assertTrue(cur_sum - 1.0 < .001 and cur_sum - 1.0 > -.001)

    def test_pick_grapheme(self):
        test_language = Language( None, script_type="no_script")
        used = []
        unused = ['a', 'b', 'c', 'd']
        g, used2, unused2 = test_language.pick_grapheme(used.copy(), unused.copy())
        self.assertTrue(type(g) is str)
        self.assertFalse(g in unused2)
        self.assertTrue(g in used2)

    def test_create_language_family(self):
        test_language = Language(None, name="Testlish", script_type="no_script")
        family = test_language.create_language_family(None)
        self.assertTrue(type(family) is str)
        self.assertTrue(family == "Testlish")

    def test_export(self):
        test1 = Language( None, script_type="no_script")
        json_data = test1.serialize_to_json()
        export_to_file(json_data, file="test_saves/test_lang.json")
        with open('test_saves/test_lang.json', 'r') as save:
            test2_json = json.load(save)
        test2 = Language(None, json=test2_json)
        self.assertTrue(test1 == test2)
        test3 = Language( None, script_type="alphabet")
        json_data2 = test3.serialize_to_json()
        export_to_file(json_data2, file="test_saves/test_alphabet_lang.json")
        with open ('test_saves/test_alphabet_lang.json', 'r') as save:
            test4_json = json.load(save)
        test4 = Language(None, json=test4_json)
        self.assertTrue(test3 == test4)

    def test_leak(self):
        test1 = Language(None)
        self.assertFalse("Testlish" in test1.word_bag.keys())

    def test_difference(self):
        base_lang = Language(None, name="Base", script_type="no_script")
        match = 0
        for i in range(0, 10):
            other_lang = Language(None, name="Other", script_type="no_script")
            if base_lang == other_lang:
                match += 1
        print("Matched: %d/10" % match)
        self.assertTrue(match < 1)




if __name__ == '__main__':
    unittest.main()