import random
# from nltk.corpus import words
wordlistfile1 = open('corncob_lowercase.txt', 'r')
wordlistfile2 = open('nederlands.txt', 'r')
wordlist1 = list()
wordlist2 = list()
out_high = open('dutchLexHigh.txt','w')
out_low = open('engLexLow2.txt', 'w')
# print words.words()[0]
def main():
	for line in wordlistfile1:
		wordlist1.append(line[:-2])
	for line in wordlistfile2:
		wordlist2.append(line[:-2])

	low_words = dict()
	high_words = dict()
	used = list()
	print("Generating common words")
	for t in range(1,100):
		w = pick_word(used, 1)
		x = pick_word(used, 2)
		low_words[w] = 1
		high_words[x] = 1
	# print("Generating rare words low")
	# # for t in range(1,25):
	# # 	w = pick_word(used, 1)
	# # 	x = pick_word(used, 2)
	# # 	low_words[w] = .5
	# # 	high_words[x] = 1
	# print("Generating rare words high")
	# for t in range(1,25):
	# 	w = pick_word(used)
	# 	low_words[w] = 1
	# 	high_words[w] = .5
	# print("Generating unique words")
	# for t in range(1,25):
	# 	w = pick_word(used)
	# 	low_words[w] = 1
	# 	x = pick_word(used)
	# 	high_words[x] = 1
	# print("Low words:")
	print("Writing to file")
	for w in low_words:
		# print w + " " + str(low_words[w])
		out_low.write(w + " " + str(low_words[w]))
		out_low.write("\n")
	# print("\n")
	# print("High Words:")
	for w in high_words:
		out_high.write(w + " " + str(high_words[w]))
		out_high.write("\n")

		# print w + " " + str(high_words[w])
	out_low.close()
	out_high.close()

def pick_word(used, num):
	if num == 1:
		l = wordlist1
	else:
		l = wordlist2
	w = random.choice(l)
	while w in used:
		w = random.choice(l)
	used.append(w)
	return w	


main()