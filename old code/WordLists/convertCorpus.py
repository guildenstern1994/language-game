import sys
import os
import codecs
sys.path.append(os.path.abspath("../IPA_Mappings/"))
# from letterMapping import consonantsIPAToInternal
# from letterMapping import vowelsIPAToInternal
# from letterMapping import consonantsInternalToIPA
# from letterMapping import vowelsInternalToIPA
from letterMapping import IPAToInternal
from letterMapping import InternalToIPA

inFile = codecs.open('testCorpusIPA.txt', 'r', 'utf-8').read()
outFile = codecs.open('testCorpusOut.txt', 'w', 'utf-8')
soup = inFile.split()
for word in soup:
	outArr = []
	for letter in word:
		# letter = let.decode('utf-8')
		if letter == 'g':
			letter = u'\u0261'
		err = False
		if letter == '\'' or letter == '\n':
			continue			
		else:
			if letter in IPAToInternal:
				conv = IPAToInternal[letter]
			# elif letter in vowelsIPAToInternal:
			# 	conv = vowelsIPAToInternal[letter]
			else:
				err = True
				print "Error: " + letter
			if not err:
				outArr.append(conv)
	string = ""
	for l in outArr:
		string += InternalToIPA[l]
	print string
	outFile.write(str(outArr))
	outFile.write('\n')
outFile.close()
# inFile.close()