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
import copy
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

def isProb(goal):
	prob = random.random()
	ret = False
	if prob < goal:
		ret = True
	return ret

class Agent(object):

	def __init__(self, caste, lexicon):
		self.caste = caste
		self.lexicon = lexicon
		
		calculate_frequency(self)
		self.semLex = dict()
		for word in self.lexicon:
			self.semLex[word.semantic] = word	



	def talk(self, agent):


		#TODO new talk function
		# MOD = (1.5 if self.caste == agent.caste else 1) * (.5 if self.caste > agent.caste else 1) * (2 if self.caste < agent.caste else 1)
		# PERM = (3 if self.caste < agent.caste else 1)
		toTell = []
		chosen = random.sample(tuple(self.lexicon), 5)

		for i in chosen:

			prob = random.random()
			w = i
			# print i
			done = False
			if isProb(.05) and not done:
				# print i
				# if i not in self.lexicon:
					# print "surprise"
				# print "sem check"
				# print self.semLex[i.semantic]
				w = discont_assimilate(i, self)
				done = True
			if isProb(.01) and not done:
				w = cont_assimilate(i, self)
				done = True
			if isProb(.01) and not done:
				w = dissimilate(i, self)
				done = True
			if isProb(.05) and not done: #this should be less random, or at least check for bigram freq between phonemes
				w = metathesis(i, self)
				done = True
			toTell.append(w)
		tell(toTell, agent)

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
		self.semantic = hash(ipa)
		self.internal = internal


def tell(wordList, agent):
	for word in wordList:

		if word not in agent.lexicon:
			# print "new word?"
			if word.semantic in agent.semLex:
				# print "semantic match"
				prob = random.random()
				if prob < .5:
					print "learned %s" % word.ipa
					agent.lexicon.remove(agent.semLex[word.semantic])
					agent.lexicon.add(word)
					# print type(word)
					agent.semLex[word.semantic] = word
					calculate_frequency(agent)


def calculate_frequency(agent):
	pi = defaultdict(lambda:0.0)
	for word in agent.lexicon:
		encoding = tuple(word.internal)

		for l in encoding:
			pi[l] += 1.0
	agent.lexSize = len(agent.lexicon)
		# print agent.lexSize
	for phon in pi:
		# print pi[phon]
		pi[phon] = pi[phon] / agent.lexSize
	agent.phoneticInventory = pi


#change phoneme to similar phoneme
def discont_assimilate(word, agent):
	#TODO Make dependent on frequency
	# print word
	# print word.semantic
	# print "sem confirm"
	# print agent.semLex[word.semantic]
	# print word.ipa
	# print word.parent

	# if word not in agent.lexicon:
		# print "line 184"
		# if agent.semLex[word.semantic] in agent.lexicon:
			# print agent.semLex[word.semantic].ipa
			# print "confusion"
			# print agent.semLex[word.semantic].parent
		# print word
	phon = random.choice(word.internal)
	change = [-.5] * 10 + [.5] * 10 + [-1] * 5 + [1] * 5
	new_phon = phon
	new_phon += random.choice(change)
	new_word = word.internal[:]
	for i in range(0, len(word.internal)):
		# print word.internal[i]
		# print phon
		if word.internal[i] == phon:
			# print "WOO"
			new_word[i] = new_phon
	# print phon
	# print new_phon
	# print new_word
	# print word.internal
	# print '\n'
	# print "changed from %s to %s"% str(word.internal), str(new_word)
	legal = check_legal(new_phon, new_word, agent)
	if legal:
		# print "legal assimilation"
		word = update_word(word, new_word, agent)
		# print "illegal assimilation"
	return word

#change phoneme to copy next or previous similar phoneme eg comnubium -> connubium
def cont_assimilate(word, agent):
	try:
		ind = random.choice(range(1, len(word.internal) - 1))
	except IndexError:
		return word
	comp = ind + 1
	left = True
	if random.random() > .75:
		comp = ind - 1
		left = False
	if check_Distance(word.internal[ind], word.internal[comp], 100):
		if left:
			substr = word.internal[ind:comp+2]
			newsubstr = substr[:]
			newsubstr[0] = substr[1]
			# substr[0] = substr[1]
			if (comp + 2) > len(word.internal):
				return word
		else:
			substr = word.internal[comp:ind+2]
			newsubstr = substr[:]
			newsubstr[1] = substr[0]
			# substr[1] = substr[0]
			if (ind + 2) > len(word.internal):
				return word

		# print "Old Word: " + word.ipa
		new_word =[]
		l = 0
		while l < len(word.internal):
			# print l
			if (l + 3) <= len(word.internal):
				# print substr
				if word.internal[l] == substr[0] and word.internal[l+1] == substr[1] and word.internal[l+2] == substr[2]:
					for let in newsubstr:
						new_word.append(let)
					l += 2
				else:
					new_word.append(word.internal[l])
			else:
				new_word.append(word.internal[l])
			l += 1

		# sInd = word.internal.find(substr)
		# new_word = word.internal[:sInd]
		# new_word += substr
		# new_word += word.internal[sInd+3:]
		# print word.internal
		# print new_word
		word = update_word(word, new_word, agent)
		# print "New Word: " + word.ipa
		for w in agent.lexicon:
			if len(w.internal) > 3:
				change = False
				new_word =[]
				l = 0
				while l < len(w.internal):
					if l + 3 <= len(w.internal):
						# print substr
						if w.internal[l] == substr[0] and w.internal[l+1] == substr[1] and w.internal[l+2] == substr[2]:
							# new_word = w.internal[:l]
							for let in newsubstr:
								new_word.append(let)
							change = True
							l += 2
						else:
							new_word.append(w.internal[l])
					else: 
						new_word.append(w.internal[l])
					l += 1
				# sInd = w.internal.find(substr)
				# new_word = w.internal[:sInd]
				# new_word += substr
				# new_word += w.internal[sInd+3:]
				if change:
					# print "Old Word: " + w.ipa
					w = update_word(w, new_word, agent)
					# print "New Word: " + w.ipa

	return word

def dissimilate(word, agent):
	l1 = random.choice(word.internal)
	l2 = random.choice(word.internal)
	ind1 = word.internal.index(l1)
	ind2 = word.internal.index(l2)
	if l1 == l2: #exit without change
		if abs(ind1 - ind2) == 1:
			return word
	if check_Distance(l1, l2, 50):
		mod = 1
		change = [1] * 5 + [10] * 2 + [100] * 2 + [150] * 2
		if ((l1 - int(l1)) - (l2 - int(l2))) == 0:
			# print "CASE"
			change += [.5] * 10 + [.25] * 10
		if l1 > l2:
			mod = -1
		prob = random.random()
		if prob < .5:
				l1 -= random.choice(change) * mod
				# DO SHIFT LEFT
		elif prob > .95:
				# DO SHIFT BOTH 
				l1 -= random.choice(change) * mod
				l2 += random.choice(change) * mod
		else:
			l2 += random.choice(change) * mod
				# DO SHIFT RIGHT
		newWord = word.internal[:]
		newWord[ind1] = l1
		newWord[ind2] = l2
		if check_legal(l1, word, agent) and check_legal(l2, word, agent):
			# print "Old: " + word.ipa
			# print InternalToIPA[l1]
			# print InternalToIPA[l2]
			word = update_word(word, newWord, agent)
			# print "New: " + word.ipa
	return word

def metathesis(word, agent):
	if len(word.internal) < 3 and len(word.internal) != 0:
		return word
	if isProb(.3):
		return hyperthesis(word, agent)
	l1 = random.choice(range(1, len(word.internal) - 1))
	l2 = l1 + 1
	while l2 < len(word.internal) - 1 and word.internal[l2] >= 2000:
		if isProb(.5):
			break
		else:
			l2 += 1
	if not redundant(l1, l2, word.internal):
		newWord = word.internal[:]
		newWord.pop(l2)
		newWord.insert(l1, word.internal[l2])
		# print "Metathesis"
		# print "Old: " + word.ipa
		word = update_word(word, newWord, agent)
		# print "New: " + word.ipa
	return word



def hyperthesis(word, agent):
	l1 = random.choice(range(1, len(word.internal) - 1))
	l2 = random.choice(range(1, len(word.internal) - 1))
	newWord = word.internal[:]
	if check_Distance(word.internal[l1], word.internal[l2], 700) and not redundant(l1, l2, word.internal) and word.internal[l1] != word.internal[l1+1]:
		# print "Hyperthesis"
		# print "Old: " + word.ipa
		newWord[l1] = word.internal[l2]
		newWord[l2] = word.internal[l1]
		word = update_word(word, newWord, agent)
		# print "New: " + word.ipa
	return word

def redundant(l1, l2, word):
	if word[l1] == word[l2]:
		return True
	elif word[l1 - 1] == word[l1] or word[l1 - 1] == word[l2]:
		return True
	elif word[l2 - 1] == word[l2]:
		return True
	else:
		return False


def check_Distance(first, second, dist):
	d = abs(first - second)
	if d < dist and d != 0:
		return True
	else:
		return False
	

def check_legal(phon, word, agent):
	if agent.phoneticInventory[phon] < 0.01:
		# print "no phoneme %s" % phon
		# print agent.phoneticInventory
		return False
	# for w in agent.lexicon:
		# if w.internal == word:
			# print "found copy of %s" % w.ipa
			# print "original %s" % oldIPA
			# return False
	# print "legal!"
	return True

def update_word(word, newInternal, agent):
	newIPA = ''
	for l in newInternal:
		newIPA += InternalToIPA[l]
	# print "Change occurred from"
	# print word.ipa
	# print newIPA
	new_word = copy.deepcopy(word)
	new_word.grandparent = word.parent
	new_word.parent = word.ipa
	new_word.ipa = newIPA
	new_word.internal = newInternal
	agent.lexicon.remove(word)
	agent.lexicon.add(new_word)
	agent.semLex[new_word.semantic] = new_word
	# print "updated"
	return new_word




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

# print "Agent: "
# a = agents[0]
# for word in a.lexicon:
# 	print word.ipa
# 	print word.internal
# 	print "\n"
# for p in a.phoneticInventory:
# 	print p
# 	print a.phoneticInventory[p]
# 	print '\n'
# for i in range(0,9):
# 	lowAgents.append(Agent(0, lowLex.copy()))
# 	highAgents.append(Agent(1, highLex.copy()))

# allAgents = lowAgents + highAgents

for i in range(0,10000):
	alice, bob = numpy.random.choice(agents, 2)
	alice.talk(bob)
	bob.talk(alice)
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
