import json
import uuid
from libs.ipaBook import ipa_book
from libs.alphabetBook import alphabet_book

def read_ipa_book():
    ipa = dict()
    for phoneme_block in ipa_book:
        ipa[phoneme_block["IPA Number"]] = phoneme_block
    return ipa


def read_alphabets():
    return alphabet_book

def convert_index_to_ipa(index_list):
    string_form = ''
    for elem in index_list:
        string_form += IPA[elem]["Character"]
    return string_form

def export_to_file(json_data, file=None):
    '''
    TODO: update architecture for use in the actual game
    '''
    if 'name' in json_data.keys():
        filename = json_data['name'] + str(uuid.uuid4()) + '.json'
    elif 'uuid' in json_data.keys():
        filename = json_data['uuid'] + str(uuid.uuid4()) + '.json'
    else:
        raise(KeyError, "Could not find name or uuid field in json")
    if file == None:
        file = filename
    with open(file, "w") as f:
        json.dump(json_data, f, indent = 4,
           ensure_ascii = False)

IPA = read_ipa_book()
ALPHABETS = read_alphabets()