### USAGE: python3 nlp.py

import nltk
from nltk import tokenize, grammar, parse, chunk, pos_tag
#from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn

##########

grammar = r"""
	JP:
		{<RB>*<JJ.*>}
	NP:
		{<DT|PRP\$>?<CD>?(<NN.*>|<JP>|<VB[GN]>)*<NN.*>}
	NP:
		{(<NP><,>)*<NP><,>?<CC><NP>}
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

#stopwords = stopwords.words('english')
#stopwords = [line.strip() for line in open('stopwords.txt', 'r').readlines()]
stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now', 'let', 'go', 'none']

#stemmer = nltk.stem.porter.PorterStemmer()
#lemmatizer = nltk.WordNetLemmatizer()

########## functions related to parsing/chunking

def leaves(tree):
	"""Finds NP (nounphrase) leaf nodes of a chunk tree."""
	for subtree in tree.subtrees(filter = lambda t: t.label()=='NP'):
		yield subtree.leaves()
 
def norm(word):
	"""Normalises words to lowercase and stems and lemmatizes it."""
	word = word.lower()
	#word = stemmer.stem_word(word)
	#word = lemmatizer.lemmatize(word)
	return word
 
def acceptableWord(word):
	"""Checks conditions for acceptable word: length, stopword."""
	accepted = bool(2 <= len(word) <= 40
	)#	and word.lower() not in stopwords)
	return accepted
 
 
def getTerms(tree):
	for leaf in leaves(tree):
		#term = [ norm(w) for w,t in leaf if acceptableWord(w) ]
		term = [ norm(w) for w,t in leaf ]
		yield term

def nps(s):
	toks = nltk.tokenize.word_tokenize(s)
	postoks = pos_tag(toks)
	#print(postoks)
 
	chunker = nltk.RegexpParser(grammar)
	tree = chunker.parse(postoks)
	#print(tree)

	terms = getTerms(tree)

	ret = []
	for term in terms:
		ret.append(' '.join(term))

	return ret

def getQClass(s):
	classfeats = []
	toks = nltk.tokenize.word_tokenize(s)
	postoks = pos_tag(toks)
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

def getRels(base):
	sss = []
	sss += [base]
#	sss += base.hypernyms()
#	sss += base.instance_hypernyms()
#	#sss += base.hyponyms()
#	#sss += base.instance_hyponyms()
#	sss += base.member_holonyms()
#	sss += base.substance_holonyms()
#	sss += base.part_holonyms()
#	sss += base.member_meronyms()
#	sss += base.substance_meronyms()
#	sss += base.part_meronyms()
	sss += base.also_sees()

	ret = []
	for ss in sss:
		for lemma in ss.lemmas():
			ret.append(lemma)
			ret += lemma.derivationally_related_forms()
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
					#print(tokens[i+j])
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
			for ss in wn.synsets(morph, pos=wn.NOUN):
				for lem in getRels(ss):
					name = lem.name().replace('_', ' ')
					if not name in ret and not name in l and not name in stopwords and len(name)>2:
						ret.append(name)
		else:
			for n in ngrams(item):
				for gram in n:
					morph = wn.morphy('_'.join(gram.split(' ')))
					if morph:
						if not gram in ret and not gram in l:
							ret.append(gram)
						for ss in wn.synsets(morph, pos=wn.NOUN):
							for lem in getRels(ss):
								name = lem.name().replace('_', ' ')
								if not name in ret and not name in l and not name in stopwords and len(name)>2:
									ret.append(name)
#						break
#				else:
#					continue
#				break

	return l+ret

def removeRedundant(l):
	ret = []
	for i, a in enumerate(l):
		redundant = False
		for j, b in enumerate(l):
			if a in b and not a == b:
				#print(a, b)
				redundant = True
				break
		if not redundant:
			ret.append(a)
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
#text = 'clubs where I can play video games and board games'
#text = 'How will we get through this?'

#print(ngrams(text))
#print(getQClass(text))
#for term in nps(text):
#	print('>>>>', term)
#for syn in addSyns(nps(text)):
#	print('>>>', syn)
