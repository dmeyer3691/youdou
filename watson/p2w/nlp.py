### USAGE: python3 nlp.py

import nltk
from nltk import tokenize, grammar, parse, chunk, pos_tag
#from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn

##########

grammar = r"""

	NP:
		{<DT|PRP\$>?<CD>?<NN.*|JJ>*<NN.*>}

	NP:
		{(<NP><,>)*<NP><,>?<CC><NP>}

	PP:
		{<IN><NP>}

	NP:
		{<NP><PP>}

"""

#stopwords = stopwords.words('english')
stopwords = [line.strip() for line in open('stopwords.txt', 'r').readlines()]
#stemmer = nltk.stem.porter.PorterStemmer()
#lemmatizer = nltk.WordNetLemmatizer()
 
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
	toks = tokenize.word_tokenize(s)
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

def addSyns(l):
	ret = []
	for item in l:
		morph = wn.morphy('_'.join(item.split(' ')))
		if morph:
			for ss in wn.synsets(morph, pos=wn.NOUN):
				for lem in ss.lemmas():
					if not lem.name() in ret and not lem.name() in stopwords and len(lem.name())>2:
						ret.append(lem.name().replace('_', ' '))
				rels = ss.hypernyms() + ss.instance_hypernyms() + ss.hyponyms() + ss.instance_hyponyms() + ss.member_holonyms() + ss.substance_holonyms() + ss.part_holonyms() + ss.member_meronyms() + ss.substance_meronyms() + ss.part_meronyms() + ss.also_sees()
				for rel in rels:
					for lem in rel.lemmas():
						if not lem.name() in ret and not lem.name() in stopwords and len(lem.name())>2:
							ret.append(lem.name().replace('_', ' '))
	if not ret:
		for item in l:
			for tok in item.split(' '):
				morph = wn.morphy('_'.join(tok.split(' ')))
				if morph:
					for ss in wn.synsets(morph, pos=wn.NOUN):
						for lem in ss.lemmas():
							if not lem.name() in ret and not lem.name() in stopwords and len(lem.name())>2:
								ret.append(lem.name().replace('_', ' '))
						rels = ss.hypernyms() + ss.instance_hypernyms() + ss.hyponyms() + ss.instance_hyponyms() + ss.member_holonyms() + ss.substance_holonyms() + ss.part_holonyms() + ss.member_meronyms() + ss.substance_meronyms() + ss.part_meronyms() + ss.also_sees()
						for rel in rels:
							for lem in rel.lemmas():
								if not lem.name() in ret and not lem.name() in stopwords and len(lem.name())>2:
									ret.append(lem.name().replace('_', ' '))
	return l+ret

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

#for term in nps(text):
#	print(term)

#print('')

#sents = tokenize.sent_tokenize(text)
#chunks = [chunk.ne_chunk(pos_tag(tokenize.word_tokenize(s))) for s in sents]

#entities = []
#for chunk in chunks[0][2]:
#	if chunk != '':
#		item = chunk
#		entities.append(item)

#print(chunks)
#print(entities)
