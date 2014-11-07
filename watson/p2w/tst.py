import nltk
from nltk import tokenize, grammar, parse, chunk, pos_tag
from nltk.corpus import stopwords

##########

grammar = r"""
    NBAR:
        {<DT>?<NN.*|JJ>*<NN.*>}
        
    NPP:
        {<NBAR><IN><NBAR>}

	NP:
        {<NBAR>}
"""

stopwords = stopwords.words('english')
#stemmer = nltk.stem.porter.PorterStemmer()
#lemmatizer = nltk.WordNetLemmatizer()
 
def NPleaves(tree):
    """Finds NP (nounphrase) leaf nodes of a chunk tree."""
    for subtree in tree.subtrees(filter = lambda t: t.label()=='NP'):
        yield subtree.leaves()
 
def NPPleaves(tree):
    """Finds NP (nounphrase) leaf nodes of a chunk tree."""
    for subtree in tree.subtrees(filter = lambda t: t.label()=='NPP'):
        yield subtree.leaves()
 
def norm(word):
    """Normalises words to lowercase and stems and lemmatizes it."""
    word = word.lower()
    #word = stemmer.stem_word(word)
    #word = lemmatizer.lemmatize(word)
    return word
 
def acceptable_word(word):
    """Checks conditions for acceptable word: length, stopword."""
    accepted = bool(2 <= len(word) <= 40
        and word.lower() not in stopwords)
    return accepted
 
 
def getNPterms(tree):
    for leaf in NPleaves(tree):
        term = [ norm(w) for w,t in leaf if acceptable_word(w) ]
        yield term

def getNPPterms(tree):
    for leaf in NPPleaves(tree):
        term = [ norm(w) for w,t in leaf if acceptable_word(w) ]
        yield term

def nps(txt):
	toks = tokenize.word_tokenize(text)
	postoks = pos_tag(toks)
	print(postoks)
 
	chunker = nltk.RegexpParser(grammar)
	tree = chunker.parse(postoks)
	print(tree)

	terms = list(getNPPterms(tree))
	#terms = list(getNPPterms(tree)).reverse()
	return terms
	#return terms[::-1]
 

##########
 
#text = 'where can i get training for a marathon'
#text = 'i made the girl a cake'
#text = 'tell me some places i can play video games'
#text = 'How can I contact health services?'
text = 'clubs about cats'

for term in nps(text):
	print(' '.join(term))
	#print(term)

print('')

sents = tokenize.sent_tokenize(text)
chunks = [chunk.ne_chunk(pos_tag(tokenize.word_tokenize(s))) for s in sents]

entities = []
for chunk in chunks[0][2]:
	if chunk != '':
		item = chunk
		entities.append(item)

print(chunks)
#print(entities)
