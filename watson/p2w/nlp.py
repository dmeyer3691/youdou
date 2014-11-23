### USAGE: python3 nlp.py

import nltk
nltk.data.path.append('/app/nltk_data')
from nltk.corpus import wordnet as wn

##########

# NP: {<DT|PRP\$>?<CD>?(<NN.*>|<JP>|<VB[GN]>)*<NN.*>}
# NP: {<DT|PRP\$>?<CD>?<JP|VB[N]>*<NP>}
grammar = r"""
	NP:
		{<NN.*>+}
	JP:
		{<RB.*>*<JJ.*>}
	NP:
		{<DT|PRP\$|CD|JP|VB[N]>+<NP>}
	NP:
		{(<NP><,>)*<NP><,>?<CC><NP>}
	NP:
		{<RB.*>*<VB[GN]><RB.*>*<NP>}
	PP:
		{<IN|TO|RP><NP>}
	PP:
		{<RB.*>*<IN><RB|EX>}
	VP:
		{<MD>?<RB.*>*<VB[DPZ]?>+<RB.*>*<VB.*>*<EX>?<RB.*>*<IN|TO|RP>?}
	VP:
		{(<VP><,>)*<VP><,>?<CC><VP>}
	NP:
		{<RB.*>*<TO><RB.*>*<VB.*><RB.*>*<VB[GN]>*<RB.*>*}
	NP:
		{<RB.*>*<VB[GN]><RB.*>*}
	NP:
		{<NP><PP>}
	RV:
		{<WP|WDT|IN><VP>}
	NX:
		{<PRP|DT>}
	REL:
		{<RV><NP|NX>}
	NP:
		{<NP|NX><REL>}
	PRED:
		{<VP><PP>*<NP|NX|JP>*<PP>*}
	PROP:
		{<NP|NX><PRED>}
	REL:
		{<WP|WDT|WRB|IN><PROP>}
	NP:
		{<NP|NX><REL>}
	QUES:
		{<W.*><MD|VP>*<PRED|PROP><\.>*}
	QUES:
		{^<PRED|PROP><.*>*<\.>*}
	IMP:
		{<PRED>}
	VOC:
		{<,>?<NP><,>?}
	PHR:
		{<CC>*<PROP|IMP|QUES|VOC>}
	PHR:
		{(<PHR><,>)*<PHR><,>?<CC><PHR>}
	SENT:
		{^<PHR><.>*}
"""

stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'many', 'part', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now', 'let', 'go', 'none']

domainspecificstopwords = ['meet', 'meeting', 'organization', 'group', 'student', 'person', 'people', 'class', 'club', 'course']

########## functions related to parsing/chunking

# returns true if all words in string are stopwords; false if any tokens are not stopwords
def isSW(s):
	for tok in s.split(' '):
		if not tok in stopwords+domainspecificstopwords:
			return False
	return True

# returns NP (nounphrase) leaf nodes of a tree
def leaves(tree):
	ret = []
	for subtree in tree.subtrees(filter = lambda t: t.label()=='NP'):
		ret.append(list(subtree.leaves()))
	return ret

# returns rightmost NN (noun) leaf node of a NP tree
def rightmostNN(tree):
	ret = []
	for subtree in tree.subtrees(filter = lambda t: t.label()=='NP'):
		if subtree.height() == 2:
			leaves = list(subtree.leaves())
			if len(leaves) > 1 and 'NN' in leaves[-1][1]:
				ret.append([leaves[-1]])
	return ret
 
# returns normalized words
def norm(word):
	return word.lower().strip()

# returns true if conditions for acceptable word are met
def acceptableWord(word):
	return (2 <= len(word.strip()) <= 40 and not isSW(word.lower()))
 
def getTerms(tree):
	ret = []
	for leaf in leaves(tree)+rightmostNN(tree):
		term = [ norm(word) for word,tag in leaf ]
		ret.append(term)
	return ret

def nps(s):
	'''TODO: more consistently use word tokenizer instead of just splitter?'''
	toks = nltk.tokenize.word_tokenize(s)
	postoks = nltk.pos_tag(toks)
	#print(postoks)
 
	chunker = nltk.RegexpParser(grammar)
	tree = chunker.parse(postoks)
	#print(tree)

	terms = getTerms(tree)

	ret = []
	for term in terms:
		joined = ' '.join(term).strip()
		if not isSW(joined):
			ret.append(' '.join(term))

	if not ret:
		for n in ngrams(s):
			ret += n

	#print('>>>', removeRepeats(ret))
	return removeRepeats(ret)

def getQClass(s):
	classfeats = []
	toks = nltk.tokenize.word_tokenize(s)
	postoks = nltk.pos_tag(toks)
	for i in range(0, len(postoks)):
		word, pos = postoks[i]
		if word.lower() == 'how':
			if i < len(postoks)-1 and postoks[i+1][0] == 'come':
				classfeats.append('CAU')
			elif i < len(postoks)-1 and ('VB' in postoks[i+1][1] or 'MD' in postoks[i+1][1]):
				classfeats.append('MAN')
			elif i < len(postoks)-1 and 'JJ' in postoks[i+1][1]:
				classfeats.append('MEA')
		if word.lower() == 'why':
			classfeats.append('CAU')
		if word.lower() == 'which':
			classfeats.append('INS')
		if word.lower() == 'who' or word.lower() == 'whom' or word.lower() == 'whose':
			classfeats.append('PER')
		if word.lower() == 'where':
			classfeats.append('LOC')
		if word.lower() == 'when':
			classfeats.append('TIM')
		#if word.lower() == 'what':
	if not classfeats:
		classfeats.append('GEN')
	return classfeats

########## functions for getting/cleaning lists of relations and keywords

'''TODO: MAKE DICT TO MAKE THIS FUNCTION POSSIBLE'''
#def getKnownRels(base):
#	

def getBasicRels(base):
	sss = []
	sss += [base]
	sss += base.also_sees()

	ret = []
	for ss in sss:
		for lemma in ss.lemmas():
			ret.append(lemma)
			ret += lemma.derivationally_related_forms()
			ret += lemma.pertainyms()
	return ret

def getAllRels(base):
	sss = []
	sss += [base]
	sss += base.hypernyms()
	sss += base.instance_hypernyms()
	sss += base.hyponyms()
	sss += base.instance_hyponyms()
	sss += base.member_holonyms()
	sss += base.substance_holonyms()
	sss += base.part_holonyms()
	sss += base.member_meronyms()
	sss += base.substance_meronyms()
	sss += base.part_meronyms()
	sss += base.also_sees()

	ret = []
	for ss in sss:
		for lemma in ss.lemmas():
			ret.append(lemma)
			ret += lemma.derivationally_related_forms()
			ret += lemma.pertainyms()
	return ret

def ngrams(s):
	m = 5
	punc = (',', ';', ':', '.', '!', '?', '(', ')', '[', ']', '{', '}', '\"', '_', '*')
	ret = []
	s = s.replace('--', ' ')
	for c in punc:
		s = s.replace(c, ' '+c+' ')

	tokens = s.split()
	for n in range(1, min(len(tokens), m)+1):
		thisn = []
		for i in range(0, len(tokens)):
			gram = ''
			if i <= (len(tokens)-n):
				for j in range(0, n):
					tokens[i+j] = tokens[i+j].strip().lower()
					if (tokens[i+j]).startswith('\''):
						tokens[i+j] = tokens[i+j][1:]
					if (tokens[i+j]).endswith('\''):
						tokens[i+j] = tokens[i+j][0:(len(tokens[i+j])-1)]
					gram = gram + ' ' + tokens[i+j]
				gram = gram.strip()
				if not gram in thisn:
					thisn.append(gram)
		ret = [thisn] + ret
	return ret
 
def addSyns(l):
	ret = []
	for item in l:
		morph = wn.morphy('_'.join(item.split(' ')))
		if morph:
			if not morph in ret:
				ret.append(morph)
			'''TODO: add provision for known words, i.e., scope words like "club"'''
			for ss in wn.synsets(morph, pos=wn.NOUN)+wn.synsets(morph, pos=wn.ADJ):
				for lem in getBasicRels(ss):
					name = lem.name().replace('_', ' ')
					if not name in ret and not name in l and not isSW(name) and len(name)>=3:
						ret.append(name)
		else:
			for n in ngrams(item):
				for gram in n:
					if not isSW(gram):
						morph = wn.morphy('_'.join(gram.split(' ')))
						if morph:
							if not morph in ret:
								ret.append(morph)
							if not gram in ret and not gram in l:
								ret.append(gram)
							for ss in wn.synsets(morph, pos=wn.NOUN)+wn.synsets(morph, pos=wn.ADJ):
								for lem in getBasicRels(ss):
									name = lem.name().replace('_', ' ')
									if not name in ret and not name in l and not isSW(name) and len(name)>=3:
										ret.append(name)
#						break
#				else:
#					continue
#				break

	return l+ret

def propagateSyns(d):
	for k1 in sorted(d, key=len, reverse=False):
		for k2 in sorted(d, key=len, reverse=False):
			if k1 != k2 and k1 in k2:
				for i in range(0, len(d[k1])):
					toAdd = []
					for j in range(0, len(d[k2])):
						if not k1 in d[k1][i] and not d[k1][i] in d[k2][j]:
							new = d[k2][j].replace(k1, d[k1][i])
							if not new in d[k2] and not new in toAdd:
								toAdd.append(new)
					d[k2] += toAdd
	return d

def synDictFromKeys(l):
	ret = {}
	for item in l:
		val = [item]
		morph = wn.morphy('_'.join(item.split(' ')))
		if morph:
			for ss in wn.synsets(morph, pos=wn.NOUN)+wn.synsets(morph, pos=wn.ADJ):
				for lem in getBasicRels(ss):
					name = lem.name().replace('_', ' ')
					if not name in ret and not name in l and not isSW(name) and len(name)>3:
						val.append(name)
			if item in ret:
				ret[item] += val
			else:
				ret[item] = val
			ret[item] = removeRepeats(ret[item])
		else:
			if item in ret:
				ret[item] += val
			else:
				ret[item] = val
			ret[item] = removeRepeats(ret[item])
			for n in ngrams(item):
				for gram in n:
					if not isSW(gram) and not gram in l:
						morph = wn.morphy('_'.join(gram.split(' ')))
						if morph:
							val = [gram]
							for ss in wn.synsets(morph, pos=wn.NOUN)+wn.synsets(morph, pos=wn.ADJ):
								for lem in getBasicRels(ss):
									name = lem.name().replace('_', ' ')
									if not name in ret and not name in l and not isSW(name) and len(name)>3:
										val.append(name)
							if gram in ret:
								ret[gram] += val
							else:
								ret[gram] = val
							ret[gram] = removeRepeats(ret[gram])
	return propagateSyns(ret)

def removeRedundant(l):
	ret = []
	for i, a in enumerate(l):
		redundant = False
		for j, b in enumerate(l):
			if i != j and a in b:
				redundant = True
				break
		if not redundant:
			ret.append(a)
	return ret

def removeRepeats(l):
	ret = []
	for i in range(0, len(l)):
		repeat = False
		for j in range(i, len(l)):
			if i != j and l[i] == l[j]:
				repeat = True
				break
		if not repeat:
			ret.append(l[i])
	return ret

##########
 
#text = 'where can i get training for a marathon'
#text = 'i made the girl a cake'
#text = 'the girl gave me some cake'
#text = 'tell me some places i can play video games'
#text = 'How can I contact health services?'
#text = 'clubs about cats'
#text = 'groups that are about video games and board games'
#text = 'groups that play video games, card games, and board games'
#text = 'I saw the man who stole my computer.'
#text = 'I like it, but that does not mean it\'s good'
#text = 'what time is LING5601'
#text = 'the courses are on Wednesdays at twelve PM.'
#text = 'you can reach me at 16144788550'
#text = 'computer science scholarships'
#text = 'Which club is the coolest?'
#text = 'Which is the coolest club?'
#text = 'How come there is no swim team?'
#text = 'computer science scholarships available to grad students'
#text = 'what are some clubs where I can play video games and board games'
#text = 'I enjoy easy video games'
#text = 'How will we get through this?'
#text = 'arabic lawyer organization'
#text = 'and if A is useful and comes to dominate the population , then the probability of an AB individual appearing then also tends towards 100 % .'
#text = 'The apostles may have believed that Jesus walked on water: that does NOT make it true.'
#text = 'Where does the anime club meet?'

#kws = nps(text)
#syns = addSyns(kws)
#syndict = synDictFromKeys(kws)

#print(kws)
#print(syns)
#print(syndict)
#print(syndict.keys())
#for key in syndict:
#	print('>>>', key)
#	print('\t', syndict[key])

#print(ngrams(text))
#print(getQClass(text))
#for term in nps(text):
#	print('>>>>', term)
#for syn in addSyns(nps(text)):
#	print('>>>', syn)
