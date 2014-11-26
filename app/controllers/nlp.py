### USAGE: python3 nlp.py

import re
import nltk
nltk.data.path.append('/app/nltk_data')
from nltk.corpus import wordnet as wn

##########

courseRE = r'[A-Z]{3,4}[\s-]?[0-9]{3,4}'

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

scopelist = [
				['alliance', 'association', 'brigade', 'chapter', 'club', 'federation', 'fraternity', 'greek life', 'group', 'league', 'organization', 'society', 'sorority'],
				['award', 'career', 'co-op', 'employment', 'externship', 'fellowship', 'fund', 'grant', 'internship', 'job', 'research', 'scholarship', 'work'],
				['colloquium', 'conference', 'fair', 'forum', 'interview', 'meet', 'meeting', 'presentation', 'seminar', 'session', 'showcase', 'social', 'speech', 'talk'],
				['class', 'corequisite', 'course', 'credit', 'lecture', 'prerequisite', 'recitation', 'requirement', 'requisite'],
				['area', 'degree', 'field', 'focus', 'major', 'minor', 'program', 'study'],
				['doctoral', 'doctorate', 'grad', 'graduate', 'master', 'phd', 'thesis'],
				['associate', 'bachelor', 'undergrad', 'undergraduate'],
				['advisor', 'contact', 'emeritus', 'facilitator', 'faculty', 'leader', 'lecturer', 'president', 'professor', 'researcher', 'staff', 'teacher'],
				['college', 'department', 'institute', 'institution', 'office', 'university'],
				['board', 'committee', 'council', 'governance', 'government', 'leadership', 'senate'],
				['volunteer', 'community service', 'service'],
				['journal', 'magazine', 'newsletter', 'publish', 'publication', 'paper'],
				['admission', 'application', 'apply', 'curriculum vitae'],
				['cause', 'initiative', 'outreach'],
				['activity', 'involvement', 'join', 'opportunity', 'recruit'],
				['individual', 'patient', 'person', 'people', 'student']
			]

scopedict = {
				'alliance'			: 0,
				'association'		: 0,
				'brigage'			: 0,
				'chapter'			: 0,
				'club'				: 0,
				'federation'		: 0,
				'fraternity'		: 0,
				'greek life'		: 0,
				'group'				: 0,
				'league'			: 0,
				'organization'		: 0,
				'society'			: 0,
				'sorority'			: 0,
				'award'				: 1,
				'career'			: 1,
				'co-op'				: 1,
				'employment'		: 1,
				'externship'		: 1,
				'fellowship'		: 1,
				'fund'				: 1,
				'grant'				: 1,
				'internship'		: 1,
				'job'				: 1,
				'research'			: 1,
				'scholarship'		: 1,
				'work'				: 1,
				'colloquium'		: 2,
				'conference'		: 2,
				'fair'				: 2,
				'forum'				: 2,
				'interview'			: 2,
				'meet'				: 2,
				'meeting'			: 2,
				'presentation'		: 2,
				'seminar'			: 2,
				'session'			: 2,
				'showcase'			: 2,
				'social'			: 2,
				'speech'			: 2,
				'talk'				: 2,
				'class'				: 3,
				'corequisite'		: 3,
				'course'			: 3,
				'credit'			: 3,
				'lecture'			: 3,
				'prerequisite'		: 3,
				'recitation'		: 3,
				'requirement'		: 3,
				'requisite'			: 3,
				'area'				: 4,
				'degree'			: 4,
				'field'				: 4,
				'focus'				: 4,
				'major'				: 4,
				'minor'				: 4,
				'program'			: 4,
				'study'				: 4,
				'doctoral'			: 5,
				'doctorate'			: 5,
				'grad'				: 5,
				'graduate'			: 5,
				'master'			: 5,
				'phd'				: 5,
				'thesis'			: 5,
				'associate'			: 6,
				'bachelor'			: 6,
				'undergrad'			: 6,
				'undergraduate'		: 6,
				'advisor'			: 7,
				'contact'			: 7,
				'emeritus'			: 7,
				'facilitator'		: 7,
				'faculty'			: 7,
				'leader'			: 7,
				'lecturer'			: 7,
				'president'			: 7,
				'professor'			: 7,
				'researcher'		: 7,
				'staff'				: 7,
				'teacher'			: 7,
				'college'			: 8,
				'department'		: 8,
				'institute'			: 8,
				'institution'		: 8,
				'office'			: 8,
				'university'		: 8,
				'board'				: 9,
				'committee'			: 9,
				'council'			: 9,
				'governance'		: 9,
				'government'		: 9,
				'leadership'		: 9,
				'senate'			: 9,
				'volunteer'			: 10,
				'community service'	: 10,
				'service'			: 10,
				'journal'			: 11,
				'magazine'			: 11,
				'newsletter'		: 11,
				'publish'			: 11,
				'publication'		: 11,
				'paper'				: 11,
				'admission'			: 12,
				'application'		: 12,
				'apply'				: 12,
				'curriculum vitae'	: 12,
				'cause'				: 13,
				'initiative'		: 13,
				'outreach'			: 13,
				'activity'			: 14,
				'involvement'		: 14,
				'join'				: 14,
				'opportunity'		: 14,
				'recruit'			: 14,
				'individual'		: 15,
				'patient'			: 15,
				'person'			: 15,
				'people'			: 15,
				'student'			: 15
			}

########## functions related to parsing/chunking

# returns a list containing all the instances of pattern p in string s
def getInstancesOfRE(p, s):
	ret = []
	s2 = s.replace('\n', '')
	while s2:
		temp = ''
		search = re.search(p, s2, re.I)
		if search:
			inst = search.group()
			ret.append(inst)
			temp = s2.replace(inst, ' ')
		if temp == s2 or not temp:
			break
		else:
			s2 = temp
	return ret

# returns true if given word is a scopeword or morph'd version thereof; false otherwise
def isScopeWord(s):
	return	(	(s in scopedict) or
				((s.endswith('ies') or s.endswith('ied')) and (s[:-3]+'y' in scopedict)) or
				(s.endswith('ing') and (s[:-3] in scopedict)) or
				((s.endswith('es') or s.endswith('ed') or s.endswith('\'s')) and (s[:-2] in scopedict)) or
				(s.endswith('s') and (s[:-1] in scopedict))
			)

# returns true if all words in string are stopwords or scopewords; false if any tokens are not stopwords
def isSW(s):
	for tok in nltk.tokenize.word_tokenize(s):
		if not tok in stopwords and not isScopeWord(tok):
				return False
	return True

def containsCourse(s):
	if re.search(courseRE, s):
		return True
	else:
		return False

# returns an array containing the indices of scopesyns 
def relevantScopes(s):
	inds = []
	for scope in scopedict:
		if	(((scope in s) or
			(scope.endswith('y') and (scope[:-1]+'ies' in s or scope[:-1]+'ied' in s)) or
			(scope+'ing' in s or scope+'es' in s or scope+'ed' in s or scope+'\'s' in s or scope+'s' in s)) and
			(not scopedict[scope] in inds)):
			inds.append(scopedict[scope])
	if not 3 in inds and containsCourse(s):
		inds.append(3)
	ret = []
	for ind in inds:
		ret += scopelist[ind]
	return ret

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

	for inst in getInstancesOfRE(courseRE, s):
		if not inst in ret:
			ret.append(inst)

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

	tokens = nltk.tokenize.word_tokenize(s)
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
		morph = wn.morphy('_'.join(nltk.tokenize.word_tokenize(item)))
		if morph:
			spacedmorph = morph.replace('_', ' ')
			if not isSW(spacedmorph):
				if not spacedmorph in ret:
					ret.append(spacedmorph)
				for ss in wn.synsets(morph, pos=wn.NOUN)+wn.synsets(morph, pos=wn.ADJ):
					for lem in getBasicRels(ss):
						name = lem.name().replace('_', ' ')
						if not name in ret and not name in l and not isSW(name) and len(name)>=3:
							ret.append(name)
		else:
			for n in ngrams(item):
				for gram in n:
					if not isSW(gram):
						morph = wn.morphy('_'.join(nltk.tokenize.word_tokenize(gram)))
						if morph:
							spacedmorph = morph.replace('_', ' ')
							if not isSW(spacedmorph):
								if not spacedmorph in ret:
									ret.append(spacedmorph)
								if not gram in ret and not gram in l:
									ret.append(gram)
								for ss in wn.synsets(morph, pos=wn.NOUN)+wn.synsets(morph, pos=wn.ADJ):
									for lem in getBasicRels(ss):
										name = lem.name().replace('_', ' ')
										if not name in ret and not name in l and not isSW(name) and len(name)>=3:
											ret.append(name)
							break
				else:
					continue
				break

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
		morph = wn.morphy('_'.join(nltk.tokenize.word_tokenize(item)))
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
						morph = wn.morphy('_'.join(nltk.tokenize.word_tokenize(gram)))
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
#text = 'groups about video games and board games'
#text = 'groups that play video games, card games, and board games'
#text = 'I saw the man who stole my computer.'
#text = 'I like it, but that does not mean it\'s good'
#text = 'what time is LING 5601'
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
#scopes = relevantScopes(text)
#syndict = synDictFromKeys(kws)

#print(kws)
#print(syns)
#print(scopes)
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
