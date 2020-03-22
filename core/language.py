
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
import logging
from libs.core_utils import IPA, ALPHABETS
logger = logging.getLogger(__name__)


class Language(object):
    '''
    TODO: more grammar features
    '''
    def __init__(self, name, parent, nodes=[], idioms={}, word_bag={}, dialects=None, 
        phonetic_inventory=None, phonetic_probs=None, word_order=None, grammar=None, 
        script=None, script_type="alphabet", language_family=None, events=None, event_log=None, json=None):
        '''
        Parameters:
            name: str
            parent: Language() or None
        '''
        if json is not None:
            self.import_from_json(json)
        else:
            self.name = name
            self.parent = parent
            self.word_bag = word_bag
            self.idioms = idioms
            self.nodes = nodes
            self.event_log = []

      
            self.phonetic_inventory = self.create_phonetic_inventory(phonetic_inventory)
            self.phonetic_probs = self.create_phonetic_probs(phonetic_probs)
            self.word_order = self.create_word_order(word_order)
            self.grammar = self.create_grammar(grammar)
            self.script = self.create_script(script, script_type)
            self.language_family = self.create_language_family(language_family)
            self.events = self.create_events(events)

            self.map_phonemes_to_graphemes()

    def __eq__(self, other):
        if type(other) is Language:
            similarity = self.compare_language(other)
            if similarity > 80:
                return  True
        return False
    def create_phonetic_inventory(self, override_value):
        '''
        TODO tweak magic number
        '''
        if override_value is not None: return override_value
        phonetic_inventory = random.sample(IPA.keys(), 35)
        if 506 not in phonetic_inventory:
            phonetic_inventory.append(506)
        return phonetic_inventory



    def create_phonetic_probs(self, override_value):
        '''
        '''
        if override_value is not None: return override_value
        num_phonemes = len(self.phonetic_inventory)
        probs = {}
        for i in range(num_phonemes):
            phoneme = self.phonetic_inventory[i]
            probs = self.set_prob_for_phoneme(num_phonemes, probs, phoneme)
        probs = self.set_prob_for_phoneme(num_phonemes, probs, '^')
        return probs

    def set_prob_for_phoneme(self, num_phonemes, probs, phoneme1):
        '''
        helper function for create_phonetic_probs
        TODO tweak magic number

        '''
        probs[phoneme1] = {}
        prob_sum = 0
        for j in range(num_phonemes):
            phoneme2 = self.phonetic_inventory[j]
            r = random.randint(0,500)
            probs[phoneme1][phoneme2] = r
            prob_sum += r
        for phoneme2 in probs[phoneme1].keys():
            probs[phoneme1][phoneme2] = float(probs[phoneme1][phoneme2]) / float(prob_sum)
        return probs



    def create_word_order(self, override_value, word_orders=['SOV', 'SVO', 'VSO', 
        'VOS', 'OVS', 'OSV', 'UNF'], order_weights=[.41, .354, .069, .018, .008, .003, .137]):
        '''
        Default order_weights correspond to distribution of real-world languages
        '''
        if override_value is not None: return override_value
        return random.choices(word_orders, order_weights, k=1)[0]

    def create_grammar(self, override_value):
        '''
        TODO?
        '''
        if override_value is not None: return override_value
        return None

    def create_script(self, override_value, script_type, mode="standard", size=None):
        '''
        TODO add other character types and selection modes
        TODO tweak size
        '''
        if override_value is not None: return override_value
        if script_type == "no_script":
            self.script_type = "no_script"
            return []
        character_set = self.choose_character_set(mode)
        if size is None:
            size = random.choice(range(20,26))
            size = min(size, len(character_set.chars))
        if mode == "standard":
            if character_set.type == "abjad":
                #TODO
                pass
            elif character_set.type == "abugida":
                #TODO
                pass
            elif character_set.type == "alphabet":
                #TODO
                script = random.sample(character_set.chars, size)
                self.script_type = "alphabet"
                return script

            elif character_set.type == "logograph":
                #TODO
                pass
            elif character_set.type == "syllabary":
                #TODO
                pass


    def choose_character_set(self, mode="standard"):
        '''
        TODO other selection modes
        TODO other script types
        '''
        if mode == "standard" or "historic":
            keys = list(ALPHABETS.keys())
            key = random.choice(keys)
            letters = ALPHABETS[key]
        elif mode == "mix":
            #TODO
            pass
        cset = CharacterSet(letters, "alphabet")
        return cset


    def map_phonemes_to_graphemes(self):
        '''
        TODO tweak magic number, support other script types
        #TODO reverse map
        '''
        seed1 = random.uniform(0,1)
        self.phoneme_to_grapheme_map = {}
        if self.script_type == "alphabet":
            unused = self.script.copy()
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
                    grapheme1, used, unused = self.pick_grapheme(used, unused)
                    grapheme2, used, unused = self.pick_grapheme(used, unused)
                    grapheme3, used, unused = self.pick_grapheme(used, unused)
                    used_graphemes = []
                    prob_sum = 0.0
                    self.phoneme_to_grapheme_map[phoneme] = {}
                    for grapheme in [grapheme1, grapheme2, grapheme3]:
                        if grapheme not in used_graphemes:
                            prob = random.uniform(0,1)
                            # print("G: ",grapheme, " ", type(grapheme))
                            # print("PH: ", type(prob))
                            # print("PR: ", type(phoneme))
                            self.phoneme_to_grapheme_map[phoneme][grapheme] = prob
                            prob_sum += prob
                    for key in self.phoneme_to_grapheme_map[phoneme].keys():
                        self.phoneme_to_grapheme_map[phoneme][key] = self.phoneme_to_grapheme_map[phoneme][key] / prob_sum
                



    def pick_grapheme(self, used, unused):
        '''
        helper function for map_phonemes_to_graphemes()
        #TODO tweak magic numbers and improve logic for realism for graphemes longer than 1
        '''
        seed1 = random.uniform(0,1)
        seed2 = random.uniform(0,1)
        if seed1 < .9:
            if (seed2 < .8 or len(used) == 0) and len(unused) > 0:
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
            unused.remove(grapheme)
        if grapheme not in used:
            used.append(grapheme)
        return grapheme, used, unused



    def create_language_family(self, override_value):
        '''
        TODO implement dynamic update for the discovery of language families
        '''
        if override_value is not None: return override_value
        if self.parent is None:
            return self.name
        else:
            return self.parent.language_family

    def compare_language(self, language2):
        '''
        TODO tweak magic numbers
        '''
        similarity = 0.0
        phonetic_inv_mod = 35 * self.calculate_phonetic_inventory_mod(language2.phonetic_inventory)
        word_order_mod = 10 * self.calculate_word_order_mod(language2.word_order)
        grammar_mod = self.calculate_grammar_mod(language2.grammar)
        script_mod = 5 * self.calculate_script_mod(language2.script, language2.script_type)
        word_bag_mod = 50 * self.calculate_word_bag_mod(language2.word_bag)

        similarity += phonetic_inv_mod
        similarity += word_order_mod
        similarity += grammar_mod
        similarity += script_mod
        similarity += word_bag_mod

        logger.info("phonetic inventory contributed %d  to the total difference" % phonetic_inv_mod)
        logger.info("word order contributed %d  to the total difference" % word_order_mod)
        logger.info("grammar contributed %d  to the total difference" % grammar_mod)
        logger.info("script contributed %d  to the total difference" % script_mod)
        logger.info("word bag contributed %d  to the total difference" % word_bag_mod)
        logger.info("total similarity is %d" % similarity)

        return similarity

    def calculate_phonetic_inventory_mod(self, pi2):
        match = 0
        for phoneme in pi2:
            if phoneme in self.phonetic_inventory:
                match += 1
            denominator += 1
        for phoneme in self.phonetic_inventory:
            if phoneme in pi2: 
                match += 1
            denominator += 1
        return match / denominator

    def calculate_word_order_mod(self, wo2):
        if self.word_order == wo2: return 1.0
        if self.word_order == "UNF" or wo2 == "UNF": return 0.4
        wo1 = list(self.word_order)
        wo2 = list(wo2)
        match = 0
        for i in range(2):
            if wo1[i] == wo2[i]:
                match += 1
        return match / 3

    def calculate_grammar_mod(self, gr2):
        return 0

    def calculate_word_bag_mod(self, wb2):
        count = 0
        for word in self.word_bag:
            if word in wb2: #TODO test rigorously, not sure this works with a complex equality function
                count += 1
        for word2 in wb2:
            if word2 in self.word_bag:
                count += 1
        denominator = len(wb2) + len(self.word_bag)
        return float(count) / float(denominator)

    def calculate_script_mod(self, sc2, stype2):
        '''
        TODO: Support for cross-type comparisons
        TODO improve calculation
        '''
        if language.script_type != stype2: return 0.0
        count = 0
        for char in self.script:
            if char in sc2:
                count += 1
        for char in sc2:
            if char in self.script:
                count += 1
        denominator = len(sc2) + len(self.script)
        return float(count) / float(denominator)

    def generate_word(mode="default"):
        '''
        Support other script types
        write generate_meaning
        returns 

        '''
        if mode == "default":
            cur_phoneme = '^'
            phoneme_array = []
            done = False
            while not done:
                cur_phoneme = random.choice(self.phonetic_probs[cur_phoneme])
                print(cur_phoneme)
                if cur_phoneme == 506:
                    break
                phoneme_array.append(cur_phoneme)
        if self.script_type == "alphabet":
            written_form = ""
            for phoneme in phoneme_array:
                written_form += self.phoneme_to_grapheme_map[phoneme]
        meaning = self.generate_meaning()
        return {"phonemes": phoneme_array, "written_form": written_form, "meaning": meaning}


    def generate_meaning():
        '''
        TODO
        '''
        return None




    def create_events(self, override_value):
        '''
        TODO
        '''
        pass

    def import_from_json(self, json):
        '''
        Import language spec from a json file
        '''
        self.name = json['name']
        self.parent = json['parent']
        self.word_bag = json['word_bag']
        self.idioms = json['idioms']
        self.nodes = json['nodes']
        self.event_log =json['event_log']
        self.phonetic_inventory = json['phonetic_inventory']
        self.phonetic_probs = json['phonetic_probs']
        self.word_order = json['word_order']
        self.grammar = json['grammar']
        self.script = json['script']
        self.language_family = json['language_faimly']
        self.events = json['events']
        self.phoneme_to_grapheme_map = json['phoneme_to_grapheme_map']

    def serialize_to_json(self):
        json = {}
        json['name'] = self.name
        json['word_bag'] = self.parent
        json['idioms'] = self.idioms
        json['nodes'] = self.nodes
        json['event_log'] = self.event_log
        json['phonetic_inventory'] = self.phonetic_inventory
        json['phonetic_probs'] = self.phonetic_probs
        json['word_order'] = self.word_order
        json['grammar'] = self.grammar
        json['script'] = self.script
        json['language_family'] = self.language_family
        json['events'] = self.events
        json['phoneme_to_grapheme_map'] = self.phoneme_to_grapheme_map
        return json

    def export_to_file(self, file=None):
        ret = self.serialize_to_json()
        if file == None:
            file = "saves/test_lang.json"
        json.dump(ret)


class CharacterSet(object):

    def __init__(self, letters, script_type):
        self.chars = letters
        self.type = script_type

    def __eq__(self, other):
        if type(other) is CharacterSet:
            if self.chars == other.chars and self.type == other.type:
                return True
        return False

