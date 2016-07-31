import numpy
from random import random
import collections

class Agent(object):

	def __init__(self, caste, lexicon):
		self.caste = caste
		self.lexicon = lexicon

	def talk(self, agent):
		MOD = (1.5 if self.caste == agent.caste else 1) * (.5 if self.caste > agent.caste else 1)
		PERM = (3 if self.caste < agent.caste else 1)
		LOSE = (2 if self.caste == 0 else 1)
		BASE_COPY = .2

		words = []
		counts = []
		for word, count in agent.lexicon:
			words.append(word)
			counts.append(count)
		total = float(sum(counts))
		normal_counts = [i/total for i in counts]

		chosen = numpy.random.choice(words, 5, replace = False, p = normal_counts)
		for word, count in common:
			if word not in self.lexicon.keys():
				return 0

castes = [0,1,2]
lowerLexicon = collections.Counter()
lowerLexicon["hello"] = 3
lowerLexicon["goodbye"] = 2

print(lowerLexicon.most_common(2))
print(lowerLexicon.keys())
print(numpy.random.choice(4, 3, p = [.1,.8,.1,0]))