import numpy
from random import random
import collections

def randomChoice(counter){
	words = []
	counts = []
	for word in counter:
		words.append(word)
		counts.append(counter[word])
	total = float(sum(counts))
	normal_counts = [i/total for i in counts]

	return(numpy.random.choice(words, 5, replace = True, p = normal_counts))
}

class Agent(object):

	def __init__(self, caste, lexicon):
		self.caste = caste
		self.lexicon = lexicon

	def talk(self, agent):
		MOD = (1.5 if self.caste == agent.caste else 1) * (.5 if self.caste > agent.caste else 1)
		PERM = (3 if self.caste < agent.caste else 1)
		LOSE = (2 if self.caste == 0 else 1)
		BASE_COPY = .2

		chosen = randomChoice(agent.lexicon)

		for word in chosen:
			if word not in self.lexicon.keys():
				if BASE_COPY * MOD > random():
					print "WOOSH"

castes = [0,1,2]
lowerLexicon = collections.Counter()
lowerLexicon["hello"] = 3
lowerLexicon["goodbye"] = 2

alice = Agent(0, lowerLexicon)
bob = Agent(0, lowerLexicon)

print(bob.talk(alice))

print(lowerLexicon.most_common(2))
print(lowerLexicon.keys())