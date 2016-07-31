import numpy
import random
import string
import collections

VOWELS = "aeiouy"
CONSONANTS = "qwrtpsdfghjklzxcvbnm"

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
	newWord = list(word)
	for i in range(0, len(word)):
		if prob > random.random():
			#change a letter
			if VOWELS.find(newWord[i]) >= 0:
				newWord[i] = random.choice(VOWELS)
			else:
				newWord[i] = random.choice(CONSONANTS)
	return "".join(newWord)

class Agent(object):

	def __init__(self, caste, lexicon):
		self.caste = caste
		self.lexicon = lexicon

	def talk(self, agent):
		MOD = (1.5 if self.caste == agent.caste else 1) * (.5 if self.caste > agent.caste else 1)
		PERM = (3 if self.caste < agent.caste else 1)

		chosen = randomChoice(agent.lexicon)

		for word in chosen:
			if .2 * MOD > random.random():
				newWord = randomNewWord(word, .05 * PERM)
				if newWord not in self.lexicon.keys():
					self.lexicon[newWord] = agent.lexicon[word]

	def forget(self):
		LOSE = (2 if self.caste == 0 else 1)

		n = 10
		least_common = self.lexicon.most_common()[:-n-1:-1]

		for word in least_common:
			if .01 * LOSE > random.random():
				del self.lexicon[word]

lowLex = collections.Counter()
highLex = collections.Counter()


with open("WordLists/engLexLow.txt") as f:
	for line in f:
		word, freq = line.split()
		lowLex[word] = float(freq)

with open("WordLists/engLexHigh.txt") as f:
	for line in f:
		word, freq = line.split()
		highLex[word] = float(freq)

agents = []

for i in range(0,9):
	agents.append(Agent(0, lowLex.copy()))
	agents.append(Agent(1, highLex.copy()))

for i in range(0,50):
	alice, bob = numpy.random.choice(agents, 2)
	alice.talk(bob)
	bob.talk(alice)
	if i % 5 == 0:
		for agent in agents:
			agent.forget()

for agent in agents:
	print(agent.lexicon)



