from libs.ipaBook import ipa_book

def read_ipa_book():
    ipa = dict()
    for phoneme_block in ipa_book:
        ipa[phoneme_block["IPA Number"]] = phoneme_block
    return ipa


def read_alphabets():
    '''
    TODO
    '''
    pass

IPA = read_ipa_book()
ALPHABETS = read_alphabets()