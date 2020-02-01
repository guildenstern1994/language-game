from consonantsInternalToIPA import consonantsInternalToIPA
from vowelsInternalToIPA import vowelsInternalToIPA


def reverseDict(dictionary):
	ret = dict()
	for key in dictionary:
		val = dictionary[key]
		ret[val] = key
	return ret
def printDict(dictionary):
	for key in dictionary:
		print key
		print dictionary[key]
		print '\n'
def mergeDict(x,y):
	z = x.copy()
	z.update(y)
	return z

consonantsIPAToInternal = reverseDict(consonantsInternalToIPA)
vowelsIPAToInternal = reverseDict(vowelsInternalToIPA)
IPAToInternal = mergeDict(consonantsIPAToInternal, vowelsIPAToInternal)
InternalToIPA = mergeDict(consonantsInternalToIPA, vowelsInternalToIPA)
# print "consonantsInternalToIPA\n"
# printDict(consonantsInternalToIPA)
# print"vowelsInternalToIPA\n"
# printDict(vowelsInternalToIPA)
# print "consonantsIPAToInternal\n"
# printDict(consonantsIPAToInternal)
# print "vowelsIPAToInternal\n"
# printDict(vowelsIPAToInternal)


