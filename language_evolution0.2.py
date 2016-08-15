import numpy
import random
import string
import collections
from collections import defaultdict
import csv
import math
import os
import codecs
import sys
from sets import Set
sys.path.append(os.path.abspath("./IPA_Mappings/"))
from letterMapping import IPAToInternal
from letterMapping import InternalToIPA

# VOWELS = "aeiouy"
# CONSONANTS = "qwrtpsdfghjklzxcvbnm"
# with open('basePhoneticMatrixEnglish.csv', 'r') as phonMatCSV:

	# reader = csv.reader(phonMatCSV, dialect=csv.excel_tab)	
	# PHONETIC_MATRIX = [[str(e) for e in r] for r in reader]
# PHONETIC_MATRIX = list(csv.reader(open('basePhoneticMatrixEnglish.csv')))
	# print PHONETIC_MATRIX

def randomChoice(counter):
	words = []
	counts = []
	for word in counter:
		words.append(word)
		counts.append(counter[word])
	total = float(sum(counts))
	normal_counts = [i/total for i in counts]

	return(numpy.random.choice(words, 5, replace = True, p = normal_counts))

def randomNewWord(word, prob):
	newWord = ""
	for i in range(0, len(word)):
		phoneme = word[i]
		if prob <= random.random() or string.ascii_lowercase.find(phoneme) == -1:
			newWord += phoneme
		else:
			# print phoneme
			if phoneme == 'x':
				phoneme = random.choice(['k','s'])
			elif phoneme == 'q':
				phoneme = 'k'
			elif phoneme == 'c':
				phoneme = numpy.random.choice(['k','s'], 1, [.8,.2])[0]

			phoneticLocation = [(index, row.index(phoneme)) for index, row in enumerate(PHONETIC_MATRIX) if phoneme in row]
			# for a in enumerate(PHONETIC_MATRIX):
				# print a
			# print phoneme
			# print phoneticLocation
			phoneme_loc = random.choice(phoneticLocation)
			distance_list = []
			phoneme_list = []
			for (x,y) in enumerate(PHONETIC_MATRIX):
				for e in y:
					if e != '':
						dist = math.sqrt( (phoneme_loc[0] - y.index(e))**2 + ((phoneme_loc[1] - x) * 3) **2 )
						if dist != 0:
							distance_list.append(dist ** -1)
						# print x
						# print y.index(e)
						phoneme_list.append(PHONETIC_MATRIX[x][y.index(e)])
			norm = [float(j)/sum(distance_list) for j in distance_list]
			# print phoneme_list
			# print len(norm)
			# print i
			replacement = numpy.random.choice(phoneme_list, 1, norm)[0]
			if replacement == 'k':
				replacement = numpy.random.choice(['q','k','c'], 1, [.1,.5,.4])
			if replacement == 's':
				phoneme = numpy.random.choice(['c','s','x'], 1, [.2,.75,.05])
			newWord += str(replacement)



			#change a letter
			# if VOWELS.find(newWord[i]) >= 0:
			# 	newWord[i] = random.choice(VOWELS)
			# else:
			# 	newWord[i] = random.choice(CONSONANTS)
	return "".join(newWord)

class Agent(object):

#NEWNEW ADDED FIELDS
	def __init__(self, caste, lexicon):
		self.caste = caste
		self.lexicon = lexicon
		self.semLex = dict()
		pi = defaultdict(lambda:0.0)			
		#prepare semantic lexicon for later permutations, I am aware that I am mapping things to themselves
		for word in lexicon:
			self.semLex[word] = word
			encoding = tuple(word.internal)
			for l in encoding:
				pi[l] += 1.0
		self.lexSize = len(self.lexicon)
		for phon in pi:
			pi[phon] = pi[phon] / self.lexSize
		self.phoneticInventory = pi

	def talk(self, agent):
		pass
		#TODO new talk function
		# MOD = (1.5 if self.caste == agent.caste else 1) * (.5 if self.caste > agent.caste else 1) * (2 if self.caste < agent.caste else 1)
		# PERM = (3 if self.caste < agent.caste else 1)

		# chosen = randomChoice(agent.lexicon)

		# for word in chosen:
		# 	if .2 * MOD > random.random():
		# 		newWord = randomNewWord(word, .05 * PERM)
		# 		if newWord not in self.lexicon.keys():
		# 			self.lexicon[newWord] = agent.lexicon[word] + float(random.choice(range(-25,25, 5))/100.0)

	def forget(self):
		pass
		#TODO new forget function
		# LOSE = (2 if self.caste == 0 else 1)

		# n = 10
		# least_common = self.lexicon.most_common()[:-n-1:-1]

		# for word in least_common:
		# 	if .01 * LOSE > random.random():
		# 		del self.lexicon[word]

# lowLex = collections.Counter()
# highLex = collections.Counter()

class Word(object):

	def __init__(self, parent, grandparent, ipa, internal):
		self.parent = parent
		self.grandparent = grandparent
		self.ipa = ipa
		self.internal = internal

#TODO: new file read-in 
lex = Set()
f = codecs.open('WordLists/testCorpusIPA.txt', 'r', 'utf-8')
soup = f.read().split()
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
	lex.add(Word(word,word,word, outArr))
f.close()

# with open("WordLists/engLexLow.txt") as f:
# 	for line in f:
# 		word, freq = line.split()
# 		lowLex[word] = float(freq)

# with open("WordLists/dutchLexHigh.txt") as f:
# 	for line in f:
# 		word, freq = line.split()
# 		highLex[word] = float(freq)


#TODO: Casteless interactions
# lowAgents = []
# highAgents = []
agents = []
for i in range(0,9):
	agents.append(Agent(0, lex.copy()))

print "Agent: "
a = agents[0]
for word in a.lexicon:
	print word.ipa
	print word.internal
	print "\n"
for p in a.phoneticInventory:
	print p
	print a.phoneticInventory[p]
	print '\n'
# for i in range(0,9):
# 	lowAgents.append(Agent(0, lowLex.copy()))
# 	highAgents.append(Agent(1, highLex.copy()))

# allAgents = lowAgents + highAgents

# for i in range(0,1000):
# 	alice, bob = numpy.random.choice(allAgents, 2)
# 	alice.talk(bob)
# 	bob.talk(alice)
# 	if i % 5 == 0:
# 		for agent in allAgents:
# 			agent.forget()

# for agent in allAgents:
# 	print(agent.lexicon)

# newLowLex = collections.Counter()
# for agent in lowAgents:
# 	newLowLex += agent.lexicon

# newHighLex = collections.Counter()
# for agent in highAgents:
# 	newHighLex += agent.lexicon

#TODO new analysis
# print("\n\n\n\n\n\n")
# print(newLowLex.most_common(10))
# print(newHighLex.most_common(10))
# # highsimilarity = 0
# # lowsimilarity = 0
# # total = 0
# for word in newHighLex.most_common(100):
# 	# print
# 	if word[0] in highLex.keys():
# 		highsimilarity += 1
# 	if word[0] in newLowLex.keys():
# 		lowsimilarity += 1
# 	total += 1
# print total
# print highsimilarity
# print lowsimilarity
# simflot = float(highsimilarity)/float(total)
# print "High to old High lexical similarity: " + str(simflot)
# simflot = float(lowsimilarity)/float(total)
# print "High to new Low lexical similarity: " + str(simflot)

# lowlowsimilarity = 0
# total = 0
# for word in newLowLex.most_common(100):
# 	if word[0] in lowLex:
# 		lowlowsimilarity += 1
# 	total += 1
# simflot = float(lowlowsimilarity)/total
# print "Low to old Low lexical similarity: " + str(simflot)

# print(newHighLex.most_common(100))
# print(newLowLex.most_common(100))
