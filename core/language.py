
'''
Language
Purpose: Represent an average of mutually intelligible dialects
Instantiated with starting values at the beginning of the game, later determined as an average of node features. 
If nodes no longer pass certain mutual intelligibility checks (or due to certain government policies), 
nodes may split and become their own dialects, and later split off entirely into independent languages.
Example: English
'''

import json
import random
from libs.utils import IPA, ALPHABETS


class Language(object):
    def __init__(self, name, parent, nodes=[], idioms={}, word_bag={}, dialects=None, 
        phonetic_inventory=None, phonetic_probs=None word_order=None, grammar=None, 
        script=None, script_type="alphabet", has_script=True language_family=None, events=None, event_log=None):
        '''
        Parameters:
            name: str
            parent: Language() or None
        '''
        self.name = name
        self.parent = parent
        self.word_bag = word_bag
        self.idioms = idioms
        self.nodes = nodes
        self.event_log = []

        if phonetic_inventory is None:
            self.create_phonetic_inventory()
        else:
            self.phonetic_inventory = phonetic_inventory

        if phonetic_probs is None:
            self.create_phonetic_probs()
        else:
            self.phonetic_probs = phonetic_probs

        if word_order is None:
            self.create_word_order()
        else:
            self.word_order = word_order

        if grammar is None:
            self.create_grammar()
        else:
            self.grammar = grammar

        if script is None:
            self.create_script(has_script=has_script)
        else:
            self.script = script
            self.script_type = script_type

        if language_family is None:
            self.create_language_family()
        else:
            self.language_family = language_family

        if events is None:
            self.create_events()
        else:
            self.events = events

        self.map_phonemes_to_graphemes()

        

    def create_phonetic_inventory(self):
        '''
        TODO tweak magic number
        '''
        self.phonetic_inventory = random.sample(IPA.keys(), 35)
        self.phonetic_inventory.append('\0')




    def create_phonetic_probs(self):
        '''
        TODO tweak magic number
        '''
        num_phonemes = len(self.phonetic_inventory)
        probs = {}
        for i in range(num_phonemes):
            phoneme1 = self.phonetic_inventory[i]
            probs[phoneme1] = {}
            prob_sum = 0
            for j in range(num_phonemes):
                phoneme2 = self.phonetic_inventory[j]
                r = random.randint(0,500)
                probs[phoneme1][phoneme2] = r
                prob_sum += r
            for phoneme2 in probs[phoneme1].keys():
                probs[phoneme1][phoneme2] = float(probs[phoneme][phoneme2]) / float(prob_sum)

        self.phonetic_probs = probs



    def create_word_order(self, word_orders=['SOV', 'SVO', 'VSO', 
        'VOS', 'OVS', 'OSV', 'UNF']order_weights=[.41, .354, .069, .018, .008, .003, .137]):
        '''
        Default order_weights correspond to distribution of real-world languages
        '''
        self.word_order = random.choices(word_orders, order_weights, k=1)

    def create_grammar(self):
        '''
        TODO
        '''
        pass

    def create_script(self, mode="standard", size=None, has_script=True):
        '''
        TODO add other character types and selection modes
        '''
        if not has_script:
            self.script_type = "no_type"
            return []
        character_set = self.choose_character_set(mode)
        if size is None:
            size = random.choice(range(20,40))
        if mode == "standard":
            if character_set.type == "abjad":
                #TODO
                pass
            elif character_set.type == "abugida":
                #TODO
                pass
            elif character_set.type == "alphabet":
                #TODO
                self.script = random.sample(character_set.chars, size)
                self.script_type = "alphabet"

            elif character_set.type == "logograph":
                #TODO
                pass
            elif character_set.type == "syllabary"
                #TODO
                pass


    def choose_character_set(self, mode="standard"):
        '''
        TODO other selection modes
        '''
        if mode == "standard" or "historic":
            return random.choice(ALPHABETS)
        elif mode == "mix":
            #TODO
            pass

    def map_phonemes_to_graphemes(self):
        '''
        TODO tweak magic number, support other script types
        '''
        seed1 = random.uniform(0,1)
        if self.script_type == "alphabet":
            unused = self.script.copy()
            self.phoneme_to_grapheme_map = {}
            used = []
            for phoneme in self.phonetic_inventory:
                if seed1 < .5:
                    grapheme, used, unused = self.pick_grapheme(used, unused)
                    self.phoneme_to_grapheme_map[phoneme] = {grapheme: 1.0}
                elif seed1 < .9:
                    grapheme1, used, unused = self.pick_grapheme(used, unused)
                    grapheme2, used, unused = self.pick_grapheme(used, unused)
                    if grapheme1 == grapheme2:
                        self.phoneme_to_grapheme_map[phoneme] = {grapheme1: 1.0}
                    else:
                        prob1 = random.uniform(0,1)
                        prob2 = random.uniform(0,1)
                        prob_sum = prob1 + prob2
                        prob1 = prob1 / prob_sum
                        prob2 = prob2 / prob_sum
                        self.phoneme_to_grapheme_map[phoneme] = {grapheme1: prob1, grapheme2: prob2}
                else:
                    grapheme1 = self.pick_grapheme(used, unused)
                    grapheme2 = self.pick_grapheme(used, unused)
                    grapheme3 = self.pick_grapheme(used, unused)
                    used_graphemes = []
                    prob_sum = 0.0
                    for grapheme in [grapheme1, grapheme2, grapheme3]:
                        if grapheme not in used_graphemes:
                            prob = random.uniform(0,1)
                            self.phoneme_to_grapheme_map[phoneme] = {grapheme: prob}
                            prob_sum += prob
                    for key in self.phoneme_to_grapheme_map[phoneme].keys():
                        self.phoneme_to_grapheme_map[key] = self.phoneme_to_grapheme_map[key] / prob_sum
                



    def pick_grapheme(self, used, unused):
        '''
        helper function for map_phonemes_to_graphemes()
        #TODO tweak magic numbers and improve logic for realism for graphemes longer than 1
        '''
        seed1 = random.uniform(0,1)
        seed2 = random.uniform(0,1)
        if seed1 < .9:
            if seed2 < .8:
                grapheme = random.choice(unused)
            else:
                grapheme = random.choice(used)
        elif seed1 < .99:
            grapheme = random.choice(used+unused)
            grapheme += random.choice(used+unused)
        else:
            grapheme = random.choice(used+unused)
            grapheme += random.choice(used+unused)
            grapheme+= random.choice(used+unused)
        if grapheme in unused:
            unused.del(grapheme)
        elif grapheme not in uused:
            used.append(grapheme)
        return grapheme, used, unused



    def create_language_family(self):
        '''
        TODO implement dynamic update for the discovery of language families
        '''
        if self.parent is None:
            self.language_family = self.name
        else:
            self.language_family = self.parent.language_family

    def create_events(self):
        '''
        TODO
        '''
        pass




