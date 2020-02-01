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
# sys.setdefaultencoding() does not exist, here!
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')


def isProb(goal):
	prob = random.random()
	ret = False
	if prob < goal:
		ret = True
	return ret


def isVoiced(key):
	if IPAToInternal[key] - math.floor(IPAToInternal[key]) == 0:
		return False
	else:
		return True



class Word(object):

	def __init__(self, parent, grandparent, ipa, internal):
		self.parent = parent
		self.grandparent = grandparent
		self.ipa = ipa
		self.semantic = hash(ipa)
		self.internal = internal	




class Agent(object):

	def __init__(self, caste, lexicon, num):
		self.caste = caste
		self.lexicon = lexicon
		self.num = num
		self.trigrams = collections.defaultdict(lambda: 0)
		self.bitotri = collections.defaultdict()
		
		calculate_frequency(self)
		self.semLex = dict()
		self.updateFrequency()


	def updateFrequency(self):
		for word in self.lexicon:
			self.semLex[word.semantic] = word
			borderedWord = "~" + word.ipa + "/"
			for i in range(0, len(borderedWord)-3):
				tri = borderedWord[i:i+3]
				trigram = (tri[0], tri[1], tri[2])
				bigram = (tri[0], tri[1])
				self.trigrams[trigram] += 1
				if bigram in self.bitotri.keys():
					self.bitotri[bigram].add(tri[2])
				else:
					self.bitotri[bigram] = set(tri[2])






	def isolatedChange(self):
		choice = random.choice(self.trigrams.keys())
		self.openLenition(choice)
		choice = random.choice(self.trigrams.keys())
		self.sonorizationLenition(choice)


	def sonorizationLenition(self, trigram):
		focus = random.randrange(0,2)
		change = None
		isEnd = False
		isBegin = False
		if focus == 2:
			isEnd = True
		elif focus == 0:
			isBegin = True
		if isBegin and trigram[0] == "~":
			return
		if isEnd and trigram[2] == "/":
			return
		if IPAToInternal[trigram[focus]] > 99 and IPAToInternal[trigram[focus]] < 200:
			if isVoiced(trigram[focus]):
				if isProb(.5):
					change = self.spiranization(trigram, focus)
				else:
					change = self.flapping(trigram, focus)
			else:
				change = self.voicing(trigram, focus)
		elif IPAToInternal[trigram[focus]] > 499 and IPAToInternal[trigram[focus]] < 900 and not (IPAToInternal[trigram[focus]] > 599 and IPAToInternal[trigram[focus]] < 700):
			change = self.approximation(trigram, focus)
		elif IPAToInternal[trigram[focus]] > 599 and IPAToInternal[trigram[focus]] < 700:
			change = self.elision(trigram, focus)
		if change != None:
			if type(change) == tuple:
				if change[0] == "~":
					self.locReplace(trigram, change, 0)
				elif change[2] == "/":
					self.locReplace(trigram, change, 2)
				else:
					self.replace(trigram, change)
			else:
				print change



	def openLenition(self, trigram):
		focus = random.randrange(0,2)
		isEnd = False
		isBegin = False
		if focus == 2:
			isEnd = True
		elif focus == 0:
			isBegin = True
		if isBegin and trigram[0] == "~":
			return
		if isEnd and trigram[2] == "/":
			return
		done = False
		if not isBegin:
			if trigram[focus] == trigram[focus - 1] and IPAToInternal[trigram[focus]] > 99 and IPAToInternal[trigram[focus]] < 200:
				change = self.degemination(trigram, focus-1)
				done = True
		if not isEnd and not done:
			if trigram[focus] == trigram[focus+1] and IPAToInternal[trigram[focus]] > 99 and IPAToInternal[trigram[focus]] < 200:
				change = self.degemination(trigram, focus)
				done = True
		if not done:
			if IPAToInternal[trigram[focus]] > 99 and IPAToInternal[trigram[focus]] < 200:
				change = self.affrication(trigram, focus)
				done = True
			elif IPAToInternal[trigram[focus]] > 199 and IPAToInternal[trigram[focus]] < 399:
				change = self.spiranization(trigram, focus)
				done = True
			elif IPAToInternal[trigram[focus]] == 532.0 or IPAToInternal[trigram[focus]] == 532.5:
				change = self.elision(trigram, focus)
				done = True
			elif IPAToInternal[trigram[focus]] > 499 and IPAToInternal[trigram[focus]] < 600:
				change = self.debuccalization(trigram, focus)
				done = True
		if done:
			if type(change) == tuple:
				if change[0] == "~":
					self.locReplace(trigram, change, 0)
				elif change[2] == "/":
					self.locReplace(trigram, change, 2)
				else:
					self.replace(trigram, change)
			else:
				print change

	def degemination(self, trigram, start):
		trigram = list(trigram)
		trigram[start] = "-"
		trigram = tuple(trigram)
		print ""
		print "Degemination occured"
		return trigram

	def approximation(self, trigram, loc):
		val = IPAToInternal[trigram[loc]]
		while val > 100:
			val -= 100
		val += 600
		if val in InternalToIPA:
			rep = InternalToIPA[val]
		else: return "illegal approximation" + str(IPAToInternal[trigram[loc]])
		trigram = list(trigram)
		trigram[loc] = rep
		trigram = tuple(trigram)
		print ""
		print "Approximation occured"
		return trigram

	def voicing(self, trigram, loc):
		if (IPAToInternal[trigram[loc]] + .5 ) in InternalToIPA:
			rep = InternalToIPA[IPAToInternal[trigram[loc]] + .5 ]
		else: return "illegal voicing" + str(IPAToInternal[trigram[loc]] )
		trigram = list(trigram)
		trigram[loc] = rep
		trigram = tuple(trigram)
		print ""
		print "Voicing occured"
		return trigram

	def affrication(self, trigram, loc):
		if (IPAToInternal[trigram[loc]] + 100 ) in InternalToIPA:
			rep = InternalToIPA[IPAToInternal[trigram[loc]] + 100 ]
		elif (IPAToInternal[trigram[loc]] + 200 ) in InternalToIPA:
			rep = InternalToIPA[IPAToInternal[trigram[loc]] + 200 ]
		else: return "illegal affrication" + str(IPAToInternal[trigram[loc]] )
		trigram = list(trigram)
		trigram[loc] = rep
		trigram = tuple(trigram)
		print ""
		print "Affrication occured"
		return trigram

	def spiranization(self, trigram, loc):
		options = set()
		if (IPAToInternal[trigram[loc]] + 400 ) in InternalToIPA:
			options.add(InternalToIPA[IPAToInternal[trigram[loc]] + 400 ])
		if (IPAToInternal[trigram[loc]] + 300 ) in InternalToIPA:
			options.add(InternalToIPA[IPAToInternal[trigram[loc]] + 300 ])
		if len(options) != 0:
			rep = random.sample(options, 1)[0]
			trigram = list(trigram)
			trigram[loc] = rep
			trigram = tuple(trigram)
			print ""
			print "Spiranization occured"
			return trigram

	def elision(self, trigram, loc):
		trigram = list(trigram)
		trigram[loc] = "-"
		trigram = tuple(trigram)
		print ""
		print "Elision occured"
		return trigram

	def flapping(self, trigram, loc):
		mod = 600
		if isVoiced(trigram[loc]):
			mod -=.5
		if (IPAToInternal[trigram[loc]] + mod ) in InternalToIPA:
			rep = InternalToIPA[IPAToInternal[trigram[loc]] + mod ]
		else: return "illegal flapping" + str(IPAToInternal[trigram[loc]] )
		trigram = list(trigram)
		trigram[loc] = rep
		trigram = tuple(trigram)
		print ""
		print "Flapping occured"
		return trigram

	def debuccalization(self, trigram, loc):
		if not isVoiced(trigram[loc]):
			rep = InternalToIPA[532.0]
		else:
			rep = InternalToIPA[532.5]
		trigram = list(trigram)
		trigram[loc] = rep
		trigram = tuple(trigram)
		print ""
		print "debuccalization occured"
		return trigram


	def replace(self, orig, new):
		if "-" in new:
			new = list(new)
			new.remove("-")
			new = tuple(new)
			elision = True
		else:
			elision = False
		origString = ''.join(orig)
		newString = ''.join(new)
		print new
		if not elision:
			internalNewString = [IPAToInternal[new[0]],IPAToInternal[new[1]],IPAToInternal[new[2]]]
		else:
			internalNewString = [IPAToInternal[new[0]],IPAToInternal[new[1]]]

		for word in self.lexicon:
			if origString in word.ipa:
				done = False
				word.grandparent = word.parent
				word.parent = word.ipa
				old = word.ipa
				while not done:
					ind = word.ipa.find(origString)
					if ind == -1:
						break
					word.ipa = word.ipa[0:ind] + newString + word.ipa[ind+3:]
					word.internal = word.internal[0:ind] + internalNewString + word.internal[ind+3:]
					self.trigrams[new] += 1
				print old + " --> " + word.ipa
				if not elision:
					if orig in self.trigrams.keys(): #hacky
						del self.trigrams[orig]
					if orig[2] in self.bitotri[(orig[0],orig[1])]: #hacky
						self.bitotri[(orig[0],orig[1])].remove(orig[2])
					if (new[0],new[1]) in self.bitotri.keys():
						self.bitotri[(new[0],new[1])].add(new[2])
					else:
						self.bitotri[(new[0], new[1])] = set(new[2])
		if elision:
			self.updateFrequency()



	def locReplace(self, orig, new, loc):
		if loc == 0:
			origString = ''.join(orig[1:])
			newString = ''.join(new[1:])
		elif loc == 2:
			newString = ''.join(new[:2])
			origString = ''.join(orig[:2])

		internalNewString = [IPAToInternal[new[0]],IPAToInternal[new[1]],IPAToInternal[new[2]]]
		for word in self.lexicon:
			if origString in word.ipa:
				ind = word.ipa.find(origString)
				if loc == 0 and ind != 0:
					continue
				elif loc == 2 and ind != len(word.ipa) - 2:
					continue
				done = False
				word.grandparent = word.parent
				word.parent = word.ipa
				old = word.ipa
				word.ipa = word.ipa[0:ind] + newString + word.ipa[ind+2:]
				word.internal = word.internal[0:ind] + internalNewString + word.internal[ind+2:]
				self.trigrams[new] += 1
				print old + " --> " + word.ipa
				del self.trigrams[orig]
				self.bitotri[(orig[0],orig[1])].pop(orig[2])
				if (new[0],new[1]) in self.bitotri.keys():
					self.bitotri[(new[0],new[1])].add(new[2])
				else:
					self.bitotri[(new[0], new[1])] = set(new[2])


def calculate_frequency(agent):
	pi = defaultdict(lambda:0.0)
	for word in agent.lexicon:
		encoding = tuple(word.internal)

		for l in encoding:
			pi[l] += 1.0
	agent.lexSize = len(agent.lexicon)
	for phon in pi:
		pi[phon] = pi[phon] / agent.lexSize
	agent.phoneticInventory = pi



##Main
IPAToInternal[u'g'] = 123.5
IPAToInternal[u'\u0320'] = 512.5
IPAToInternal[u'\u031f'] = 701.0
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
agents = []
agentNum = 50
for i in range(agentNum-1):
	agents.append(Agent(0, lex.copy(), i))


def parentExists(word, agent):
	parent = word.parent
	for w in agent.lexicon:
		if parent == w.parent:
			return True
	return False

def talk(agent1, agent2):
	words = random.sample(agent1.lexicon, 20)
	for word in words:
		if word not in agent2.lexicon:
			if parentExists(word, agent2):
				if isProb(.5):
					print "learned word " + word.ipa + " instead of " + word.parent
					agent2.lexicon.remove(word.parent)
					agent2.lexicon.add(word)
				else:
					print "learned word parent " + word.parent.ipa + " instead of " + word.ipa

					word.ipa = word.parent
					word.parent = word.grandparent
					word.grandparent = None
					# agent1.lexicon.add(word.parent)
			elif isProb(.9):
				agent2.lexicon.add(word)



numiters = 10
for i in range(0,numiters):
	print "GENERATION " + str(i)
	print "~~~~~~~~~~~~~~~~~~~~~~~~"
	for agent in agents:
		# print "AGENT " + str(agent.num)
		agent.isolatedChange()
		# print ""
	print "Talk Phase"
	for i in range((agentNum/2)-1):
		agentI = agents[i]
		agentJ = agents[i+(agentNum/2)]
		for k in range(agentNum/2):
			if i != k:
				talk(agentI, agents[k])
				talk(agents[k], agentI)
				talk(agentJ, agents[(k+agentNum/2)-1])
				talk(agents[(k+agentNum/2)-1], agentJ)



# def randomChoice(counter):
# 	words = []
# 	counts = []
# 	for word in counter:
# 		words.append(word)
# 		counts.append(counter[word])
# 	total = float(sum(counts))
# 	normal_counts = [i/total for i in counts]

# 	return(numpy.random.choice(words, 5, replace = True, p = normal_counts))

# def randomNewWord(word, prob):
# 	newWord = ""
# 	for i in range(0, len(word)):
# 		phoneme = word[i]
# 		if prob <= random.random() or string.ascii_lowercase.find(phoneme) == -1:
# 			newWord += phoneme
# 		else:
# 			# print phoneme
# 			if phoneme == 'x':
# 				phoneme = random.choice(['k','s'])
# 			elif phoneme == 'q':
# 				phoneme = 'k'
# 			elif phoneme == 'c':
# 				phoneme = numpy.random.choice(['k','s'], 1, [.8,.2])[0]

# 			phoneticLocation = [(index, row.index(phoneme)) for index, row in enumerate(PHONETIC_MATRIX) if phoneme in row]
# 			# for a in enumerate(PHONETIC_MATRIX):
# 				# print a
# 			# print phoneme
# 			# print phoneticLocation
# 			phoneme_loc = random.choice(phoneticLocation)
# 			distance_list = []
# 			phoneme_list = []
# 			for (x,y) in enumerate(PHONETIC_MATRIX):
# 				for e in y:
# 					if e != '':
# 						dist = math.sqrt( (phoneme_loc[0] - y.index(e))**2 + ((phoneme_loc[1] - x) * 3) **2 )
# 						if dist != 0:
# 							distance_list.append(dist ** -1)
# 						# print x
# 						# print y.index(e)
# 						phoneme_list.append(PHONETIC_MATRIX[x][y.index(e)])
# 			norm = [float(j)/sum(distance_list) for j in distance_list]
# 			# print phoneme_list
# 			# print len(norm)
# 			# print i
# 			replacement = numpy.random.choice(phoneme_list, 1, norm)[0]
# 			if replacement == 'k':
# 				replacement = numpy.random.choice(['q','k','c'], 1, [.1,.5,.4])
# 			if replacement == 's':
# 				phoneme = numpy.random.choice(['c','s','x'], 1, [.2,.75,.05])
# 			newWord += str(replacement)



# 			#change a letter
# 			# if VOWELS.find(newWord[i]) >= 0:
# 			# 	newWord[i] = random.choice(VOWELS)
# 			# else:
# 			# 	newWord[i] = random.choice(CONSONANTS)
# 	return "".join(newWord)


	# def talk(self, agent):


	# 	# MOD = (1.5 if self.caste == agent.caste else 1) * (.5 if self.caste > agent.caste else 1) * (2 if self.caste < agent.caste else 1)
	# 	# PERM = (3 if self.caste < agent.caste else 1)
	# 	toTell = []
	# 	chosen = random.sample(tuple(self.lexicon), 5)

	# 	for i in chosen:

	# 		prob = random.random()
	# 		w = i
	# 		# print i
	# 		done = False
	# 		#I'm thinking maybe we can get rid of done and just drop the target probability
	# 		if isProb(.05) and not done:
	# 			# print i
	# 			# if i not in self.lexicon:
	# 				# print "surprise"
	# 			# print "sem check"
	# 			# print self.semLex[i.semantic]
	# 			w = discont_assimilate(i, self)
	# 			done = True
	# 		if isProb(.01) and not done:
	# 			w = cont_assimilate(i, self)
	# 			done = True
	# 		if isProb(.01) and not done:
	# 			w = dissimilate(i, self)
	# 			done = True
	# 		if isProb(.05) and not done: #this should be less random, or at least check for bigram freq between phonemes
	# 			w = metathesis(i, self)
	# 			done = True
	# 		if isProb(.1) and not done:
	# 			w = haplogy(i, self)
	# 			done = True
	# 		#At some point tone would be nice
	# 		toTell.append(w)
	# 	tell(toTell, agent)

			# 	if .2 * MOD > random.random():
			# 		newWord = randomNewWord(word, .05 * PERM)
			# 		if newWord not in self.lexicon.keys():
			# 			self.lexicon[newWord] = agent.lexicon[word] + float(random.choice(range(-25,25, 5))/100.0)

	# def forget(self):
		# pass
		# LOSE = (2 if self.caste == 0 else 1)

		# n = 10
		# least_common = self.lexicon.most_common()[:-n-1:-1]

		# for word in least_common:
		# 	if .01 * LOSE > random.random():
		# 		del self.lexicon[word]

# lowLex = collections.Counter()
# highLex = collections.Counter()




# def tell(wordList, agent):
# 	for word in wordList:

# 		if word not in agent.lexicon:
# 			# print "new word?"
# 			if word.semantic in agent.semLex:
# 				# print "semantic match"
# 				prob = random.random()
# 				if prob < .5:
# 					print "learned %s" % word.ipa
# 					agent.lexicon.remove(agent.semLex[word.semantic])
# 					agent.lexicon.add(word)
# 					# print type(word)
# 					agent.semLex[word.semantic] = word
# 					calculate_frequency(agent)





#change phoneme to similar phoneme
# def discont_assimilate(word, agent):
# 	# print word
# 	# print word.semantic
# 	# print "sem confirm"
# 	# print agent.semLex[word.semantic]
# 	# print word.ipa
# 	# print word.parent

# 	# if word not in agent.lexicon:
# 		# print "line 184"
# 		# if agent.semLex[word.semantic] in agent.lexicon:
# 			# print agent.semLex[word.semantic].ipa
# 			# print "confusion"
# 			# print agent.semLex[word.semantic].parent
# 		# print word
# 	phon = random.choice(word.internal)
# 	change = [-.5] * 10 + [.5] * 10 + [-1] * 5 + [1] * 5
# 	new_phon = phon
# 	new_phon += random.choice(change)
# 	new_word = word.internal[:]
# 	for i in range(0, len(word.internal)):
# 		# print word.internal[i]
# 		# print phon
# 		if word.internal[i] == phon:
# 			# print "WOO"
# 			new_word[i] = new_phon
# 	# print phon
# 	# print new_phon
# 	# print new_word
# 	# print word.internal
# 	# print '\n'
# 	# print "changed from %s to %s"% str(word.internal), str(new_word)
# 	legal = check_legal(new_phon, new_word, agent)
# 	if legal:
# 		# print "legal assimilation"
# 		word = update_word(word, new_word, agent)
# 		# print "illegal assimilation"
# 	return word

# #change phoneme to copy next or previous similar phoneme eg comnubium -> connubium
# def cont_assimilate(word, agent):
# 	try:
# 		ind = random.choice(range(1, len(word.internal) - 1))
# 	except IndexError:
# 		return word
# 	comp = ind + 1
# 	left = True
# 	if random.random() > .75:
# 		comp = ind - 1
# 		left = False
# 	if check_Distance(word.internal[ind], word.internal[comp], 100):
# 		if left:
# 			substr = word.internal[ind:comp+2]
# 			newsubstr = substr[:]
# 			newsubstr[0] = substr[1]
# 			# substr[0] = substr[1]
# 			if (comp + 2) > len(word.internal):
# 				return word
# 		else:
# 			substr = word.internal[comp:ind+2]
# 			newsubstr = substr[:]
# 			newsubstr[1] = substr[0]
# 			# substr[1] = substr[0]
# 			if (ind + 2) > len(word.internal):
# 				return word

# 		# print "Old Word: " + word.ipa
# 		new_word =[]
# 		l = 0
# 		while l < len(word.internal):
# 			# print l
# 			if (l + 3) <= len(word.internal):
# 				# print substr
# 				if word.internal[l] == substr[0] and word.internal[l+1] == substr[1] and word.internal[l+2] == substr[2]:
# 					for let in newsubstr:
# 						new_word.append(let)
# 					l += 2
# 				else:
# 					new_word.append(word.internal[l])
# 			else:
# 				new_word.append(word.internal[l])
# 			l += 1

# 		# sInd = word.internal.find(substr)
# 		# new_word = word.internal[:sInd]
# 		# new_word += substr
# 		# new_word += word.internal[sInd+3:]
# 		# print word.internal
# 		# print new_word
# 		word = update_word(word, new_word, agent)
# 		# print "New Word: " + word.ipa
# 		for w in agent.lexicon:
# 			if len(w.internal) > 3:
# 				change = False
# 				new_word =[]
# 				l = 0
# 				while l < len(w.internal):
# 					if l + 3 <= len(w.internal):
# 						# print substr
# 						if w.internal[l] == substr[0] and w.internal[l+1] == substr[1] and w.internal[l+2] == substr[2]:
# 							# new_word = w.internal[:l]
# 							for let in newsubstr:
# 								new_word.append(let)
# 							change = True
# 							l += 2
# 						else:
# 							new_word.append(w.internal[l])
# 					else: 
# 						new_word.append(w.internal[l])
# 					l += 1
# 				# sInd = w.internal.find(substr)
# 				# new_word = w.internal[:sInd]
# 				# new_word += substr
# 				# new_word += w.internal[sInd+3:]
# 				if change:
# 					# print "Old Word: " + w.ipa
# 					w = update_word(w, new_word, agent)
# 					# print "New Word: " + w.ipa

# 	return word

# def dissimilate(word, agent):
# 	l1 = random.choice(word.internal)
# 	l2 = random.choice(word.internal)
# 	ind1 = word.internal.index(l1)
# 	ind2 = word.internal.index(l2)
# 	if l1 == l2: #exit without change
# 		if abs(ind1 - ind2) == 1:
# 			return word
# 	if check_Distance(l1, l2, 50):
# 		mod = 1
# 		change = [1] * 5 + [10] * 2 + [100] * 2 + [150] * 2
# 		if ((l1 - int(l1)) - (l2 - int(l2))) == 0:
# 			# print "CASE"
# 			change += [.5] * 10 + [.25] * 10
# 		if l1 > l2:
# 			mod = -1
# 		prob = random.random()
# 		if prob < .5:
# 				l1 -= random.choice(change) * mod
# 				# DO SHIFT LEFT
# 		elif prob > .95:
# 				# DO SHIFT BOTH 
# 				l1 -= random.choice(change) * mod
# 				l2 += random.choice(change) * mod
# 		else:
# 			l2 += random.choice(change) * mod
# 				# DO SHIFT RIGHT
# 		newWord = word.internal[:]
# 		newWord[ind1] = l1
# 		newWord[ind2] = l2
# 		if check_legal(l1, word, agent) and check_legal(l2, word, agent):
# 			# print "Old: " + word.ipa
# 			# print InternalToIPA[l1]
# 			# print InternalToIPA[l2]
# 			word = update_word(word, newWord, agent)
# 			# print "New: " + word.ipa
# 	return word

# def metathesis(word, agent):
# 	if len(word.internal) < 3 and len(word.internal) != 0:
# 		return word
# 	if isProb(.3):
# 		return hyperthesis(word, agent)
# 	l1 = random.choice(range(1, len(word.internal) - 1))
# 	l2 = l1 + 1
# 	while l2 < len(word.internal) - 1 and word.internal[l2] >= 2000:
# 		if isProb(.5):
# 			break
# 		else:
# 			l2 += 1
# 	if not redundant(l1, l2, word.internal):
# 		newWord = word.internal[:]
# 		if l2 < len(newWord) - 1 and newWord[l2] < 2000 and newWord[l1+1] > 2000 and newWord[l2+1] > 2000:
# 			# print 'FANCY'
# 			newWord.pop(l2)
# 			newWord.pop(l2)
# 			newWord.insert(l1, word.internal[l2+1])
# 			newWord.insert(l1, word.internal[l2])
# 		else:
# 			newWord.pop(l2)
# 			newWord.insert(l1, word.internal[l2])
# 		# print "Metathesis"
# 		# print "Old: " + word.ipa
# 		if l2 < len(newWord)-1:
# 			if newWord[l2] > 2000 and newWord[l2+1] > 2000:
# 				if isProb(.75):
# 					newWord = correct_Double_Vowel(l2, newWord, agent)
# 		if l1 > 0:
# 			if newWord[l1] > 2000 and newWord[l1-1] > 2000:
# 				if isProb(.75):
# 					newWord = correct_Double_Vowel(l1-1, newWord, agent)
# 		word = update_word(word, newWord, agent)
# 		# print "New: " + word.ipa
# 	return word

# def correct_Double_Vowel(loc, w, agent):
# 	# print "problem"
# 	# print w
# 	prob = random.random()
# 	if prob < .25:
# 		w.pop(loc)
# 	elif prob < .5:
# 		w.pop(loc+1)
# 	else:
# 		l1 = w[loc]
# 		l2 = w[loc + 1]
# 		mid = (l1 + l2) / 2.0
# 		mid = int(mid)
# 		mid = float(mid)
# 		w.pop(loc+1)
# 		direction = random.choice([-.5, .5])
# 		while mid not in InternalToIPA:
# 			mid += direction
# 			if mid not in agent.phoneticInventory:
# 				if isProb(.25):
# 					# print mid
# 					mid += direction

# 		w[loc] = mid
# 	# print "solution"
# 	# print w
# 	return w


# def hyperthesis(word, agent):
# 	l1 = random.choice(range(1, len(word.internal) - 1))
# 	l2 = random.choice(range(1, len(word.internal) - 1))
# 	newWord = word.internal[:]
# 	if check_Distance(word.internal[l1], word.internal[l2], 700) and not redundant(l1, l2, word.internal) and word.internal[l1] != word.internal[l1+1]:
# 		# print "Hyperthesis"
# 		# print "Old: " + word.ipa
# 		newWord[l1] = word.internal[l2]
# 		newWord[l2] = word.internal[l1]
# 		word = update_word(word, newWord, agent)
# 		# print "New: " + word.ipa
# 	return word

# def haplogy(word, agent):
# 	if len(word.internal) < 6:
# 		return word
# 	l1 = random.choice(range(1, len(word.internal) - 4))
# 	l2 = l1 + 1
# 	l3 = l2 + 1
# 	l4 = l3 + 1
# 	if word.internal[l1] == word.internal[l3]:
# 		if check_Distance(word.internal[l2], word.internal[l4], 50) or word.internal[l2] == 2303.0:
# 			print "Old: "  + word.ipa
# 			newWord = word.internal[:]
# 			newWord.pop(l1)
# 			newWord.pop(l1)
# 			word = update_word(word, newWord, agent)
# 			print "New: " + word.ipa
# 	return word

# def redundant(l1, l2, word):
# 	if word[l1] == word[l2]:
# 		return True
# 	elif word[l1 - 1] == word[l1] or word[l1 - 1] == word[l2]:
# 		return True
# 	elif word[l2 - 1] == word[l2]:
# 		return True
# 	else:
# 		return False


# def check_Distance(first, second, dist):
# 	d = abs(first - second)
# 	if d < dist and d != 0:
# 		return True
# 	else:
# 		return False
	

# def check_legal(phon, word, agent):
# 	if agent.phoneticInventory[phon] < 0.01:
# 		# print "no phoneme %s" % phon
# 		# print agent.phoneticInventory
# 		return False
# 	# for w in agent.lexicon:
# 		# if w.internal == word:
# 			# print "found copy of %s" % w.ipa
# 			# print "original %s" % oldIPA
# 			# return False
# 	# print "legal!"
# 	return True

# def update_word(word, newInternal, agent):
# 	newIPA = ''
# 	for l in newInternal:
# 		newIPA += InternalToIPA[l]
# 	# print "Change occurred from"
# 	# print word.ipa
# 	# print newIPA
# 	new_word = copy.deepcopy(word)
# 	new_word.grandparent = word.parent
# 	new_word.parent = word.ipa
# 	new_word.ipa = newIPA
# 	new_word.internal = newInternal
# 	agent.lexicon.remove(word)
# 	agent.lexicon.add(new_word)
# 	agent.semLex[new_word.semantic] = new_word
# 	# print "updated"
# 	return new_word






# with open("WordLists/engLexLow.txt") as f:
# 	for line in f:
# 		word, freq = line.split()
# 		lowLex[word] = float(freq)

# with open("WordLists/dutchLexHigh.txt") as f:
# 	for line in f:
# 		word, freq = line.split()
# 		highLex[word] = float(freq)


# lowAgents = []
# highAgents = []

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







# for i in range(0,10000):
# 	alice, bob = numpy.random.choice(agents, 2)
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
