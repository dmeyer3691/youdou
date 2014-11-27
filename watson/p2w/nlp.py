### USAGE: python3 nlp.py

import re
import nltk
nltk.data.path.append('/app/nltk_data')
from nltk.corpus import wordnet as wn

##########

########## REs

courseRE = r'[A-Z]{3,4}[\s-]?[0-9]{3,4}'

titleTagRE = r'(<head>.*?</head>)|(<h1.*>.*?</h1>)|(<span>.*?</span>)'
#contentTagRE = r'(<p>.*?</p>)|(<tr(\s?)>.*?</tr>)|(<li>.*?</li>)'
contentTagRE = r'(<(p|br/)>.*?<(/p|br/)>)|(<tr(\s?)>.*?</tr>)|(<li>.*?</li>)'
anyTagRE = r'(<.+?>)'

##### class REs
## time
exactMTimeRE = r'((([2][0-3])|([0-1]?[0-9]))((:[0-5][0-9])|(\s+)o\'clock))|(((([2][0-3])|([0-1][0-9]))((:)?[0-5][0-9]))((\s+)hours))'
exactCTimeRE = r'((([1][0-2])|([0]?[0-9]))(:[0-5][0-9])?)(((\s*)o\'clock)|((\s*)[ap](\.)?(m)(\.)?)){1,2}'
apprxTimeRE = r'((at|exactly|around|about|before|after)(\s+))?(((a(n?))(\s))?((five|ten|quarter|half)(\s))((til|\'til|until|to|after|past)(\s)))?(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|noon|midnight)(((\s*)o\'clock)|((\s*)[ap](\.)?(m)(\.)?)){1,2}'
dayRE = r'((on|each|every|every(\s)other)(\s))?((\w)*((day(s?))|morrow))'
fullDateRE = r'(((the(\s+))?([0-3]?[0-9](st|nd|rd|th)?)(\s+)(of(\s+))?(jan(uary)?|feb(ruary)?|mar(ch)?|apr(il)?|may|jun(e)?|jul(y)?|aug(ust)?|sep((t)?ember)?|oct(ober)?|nov(ember)?|dec(ember)?)(\.?))|((jan(uary)?|feb(ruary)?|mar(ch)?|apr(il)?|may|jun(e)?|jul(y)?|aug(ust)?|sep((t)?ember)?|oct(ober)?|nov(ember)?|dec(ember)?)(\.?)(\s+)([0-3]?[0-9](st|nd|rd|th)?)))((,?)(\s*))([0-9]{4}((\s*)((b(\.?)c(\.?))|(a(\.?)d(\.?))))?)?'
condDateRE = r'((([0-3]?[0-9])(\s*)[/\-\.](\s*)([0-1]?[0-9]))|(([0-1]?[0-9])(\s*)[/\-\.](\s*)([0-3]?[0-9])))((\s*)[/\-\.](\s*)(([0-9]{2})|([0-9]{4})))?'
durationRE = r'((in|for|after)(\s+))?((about|approx(\.?)(imately)?|exactly)(\s+))?((a(n?)|the)(\s+))?((couple|few|some|many|several|lot of|next)(\s+))?((([0-9]+)|(one|two|three|four|five|six|seven|eight|nine|ten))(\s+))?(second(s?)|minute(s?)|hour(s?)|day(s?)|week(s?)|month(s?)|year(s?)|quarter(s?)|semester(s?)|season(s?))'
NNumberRE = r'([0-9]{1,3}(,?))?([0-9]{3}(,?))?([0-9]{1-3})?((\.)[0-9]+)?'
ANumberRE = r'zero|(((((((twen|thir|for|fif|six|seven|eigh|nine)(ty)(-?))?(one|two|three|four|five|six|seven|eight|nine)?)|ten|eleven|twelve|((thir|four|fif|six|seven|eigh|nine)(teen)))((\s)(point)(zero|one|two|three|four|five|six|seven|eight|nine)+)?)?(hundred|thousand|([a-z]+(illion))((\s)|(and\s)|(,\s))?))*(((((twen|thir|for|fif|six|seven|eigh|nine)(ty)(-?))?(one|two|three|four|five|six|seven|eight|nine)?)|ten|eleven|twelve|((thir|four|fif|six|seven|eigh|nine)(teen)))((\s)(point|and)(zero|one|two|three|four|five|six|seven|eight|nine)+)?))'
## contact/location
phoneNumberRE = r'(\+?)(([0-9]([\s\.-]?))?((\(?)[0-9]{3}(\)?)([\s\.-]?)))?([0-9]{3}([\s\.-]?))([0-9]{4})'
emailRE = r'([\(\[\{]\s*)*(\S+)(\s*[\)\]\}])*((\s*)(\.|(([\(\[\{]\s*)*dot([\)\]\}]\s*)*))(\s*)([\(\[\{]\s*)*(\S+)(\s*[\)\]\}])*(\s*))*(\s*)(@|(([\(\[\{]\s*)*at(sign)?([\)\]\}]\s*)*))((\s*)([\(\[\{]\s*)*(\S+)(\s*[\)\]\}])*(\s*)(\.|(([\(\[\{]\s*)*dot([\)\]\}]\s*)*)))+(\s*)([\(\[\{]\s*)*(com|edu|gov|me|info|co|net)(\s*[\)\]\}])*'
#addressRE = r'([0-9]+(\s+))?([a-z]+(\s+)){1,2}((apt|apartment|ave|avenue|ct|court|dr|drive|ln|lane|pkwy|parkway|rd|road|st|street|way)(\.?)((\s+)[a-z0-9]+)?)?(,(\s+))?(([a-z]+(\s+)){1,2}(,(\s+))[a-z]+(\s+))[0-9]{5}(-[0-9]{4})?'
addressRE = r'([0-9]+(\s+))([a-z]+(\s+)){1,2}((apartment|apt|avenue|ave|court|ct|drive|dr|gateway|gtwy|hall|lane|ln|parkway|pkwy|road|rd|street|st|way)(\.?)((\s+)[a-z0-9]+)?)((,?)(((\s+)[a-z]+){1,2}(,)(\s+)[a-z]+)?((\s+)[0-9]{5}(-[0-9]{4})?)?)?'

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

########## lexicons

stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'many', 'part', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now', 'let', 'go', 'none']

##### class lexicons
## time
generalTimeWords = ['when', 'schedule', 'hours', 'time', 'second', 'minute', 'hour', 'day', 'week', 'month', 'year', 'semester', 'quarter']
pointTimeWords = ['at', 'on', 'between']
frequencyTimeWords = ['every', 'each', 'days', 'weekends', 'yearly', 'monthly', 'daily', 'hourly', 'semesterly', 'quarterly']
durationTimeWords = ['long', 'for', 'last', 'continue']
## contact ...'meet'?
generalContactWords = ['contact', 'reach', 'talk to', 'mail', 'address', 'appointment']
emailContactWords = ['email', 'e-mail', 'message']
phoneContactWords = ['phone number', 'phone', 'call', 'number']
## location
generalLocationWords = ['where', 'location', 'located', 'place', 'building', 'center', 'floor', 'room', 'library', 'office', 'house', 'department']
## money
generalMoneyWords = ['$', 'money', 'how much', 'dollar', 'cent', 'expensive', 'cheap', 'free', 'cost', 'loan', 'pay', 'paid', 'spend', 'spent', 'fee', 'charge']
## person
generalPersonWords = ['whose', 'whom', 'who', 'mrs.', 'miss', 'mr.', 'doctor', 'dr.', 'professor', 'prof.', 'prof', 'vice president', 'v.p.', 'president', 'pres.', 'treasurer', 'leader', 'counselor', 'facilitator', 'contact']

allclasswords = generalTimeWords+pointTimeWords+frequencyTimeWords+durationTimeWords+generalContactWords+emailContactWords+phoneContactWords+generalLocationWords+generalMoneyWords+generalPersonWords
#allclasswords = generalTimeWords+pointTimeWords+frequencyTimeWords+durationTimeWords+generalContactWords+emailContactWords+phoneContactWords+generalLocationWords+generalMoneyWords

##### scope lexicon
scopelist = [
				['alliance', 'association', 'brigade', 'chapter', 'club', 'federation', 'fraternity', 'greek life', 'group', 'league', 'organization', 'society', 'sorority'],
				['award', 'career', 'co-op', 'employment', 'externship', 'fellowship', 'fund', 'grant', 'internship', 'job', 'research', 'scholarship', 'work'],
				['colloquium', 'conference', 'fair', 'forum', 'interview', 'meet', 'meeting', 'presentation', 'seminar', 'session', 'showcase', 'social', 'speech', 'talk'],
				['class', 'corequisite', 'course', 'credit', 'lecture', 'prerequisite', 'recitation', 'requirement', 'requisite'],
				['area', 'degree', 'field', 'focus', 'major', 'minor', 'program', 'study'],
				['doctoral', 'doctorate', 'grad', 'graduate', 'master', 'phd', 'thesis'],
				['associate', 'bachelor', 'undergrad', 'undergraduate'],
				['advisor', 'contact', 'counselor', 'emeritus', 'facilitator', 'faculty', 'leader', 'lecturer', 'president', 'professor', 'researcher', 'staff', 'teacher'],
				['college', 'department', 'institute', 'institution', 'office', 'university'],
				['board', 'committee', 'council', 'governance', 'government', 'in charge of', 'leadership', 'senate'],
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
				'counselor'			: 7,
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
				'in charge of'		: 9,
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

# returns true if given word is a classword or morph'd version thereof; false otherwise
def isClassWord(s):
	return	(	(s in allclasswords) or
				((s.endswith('ies') or s.endswith('ied')) and (s[:-3]+'y' in allclasswords)) or
				(s.endswith('ing') and (s[:-3] in allclasswords)) or
				((s.endswith('es') or s.endswith('ed') or s.endswith('\'s')) and (s[:-2] in allclasswords)) or
				(s.endswith('s') and (s[:-1] in allclasswords))
			)

# returns true if all words in string are stopwords or scopewords; false if any tokens are not stopwords
def isSW(s):
	for tok in nltk.tokenize.word_tokenize(s):
		if not tok in stopwords and not isScopeWord(tok) and not isClassWord(tok):
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
					#for lem in getAllRels(ss):
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
									#for lem in getAllRels(ss):
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

########## general tools (FORMERLY IN KW.PY)

# returns html sans titleish thing
def removeStuffFromHTML(s):
	#return re.compile(titleTagRE).sub('', s.replace('\n', '<br/>')).strip()
	return re.compile(titleTagRE).sub('', s.replace('\n', '').replace('<br/>.', '<br/>').replace('Tweet.', '')).strip()

def rawFromHTML(s):
	return ' '.join(re.compile(anyTagRE).sub(' ', s).split()).strip()

def getContentHTML(s, syns, scopes, query):
	allcontent = getInstancesOfRE(contentTagRE, s)
	if not allcontent:
		allcontent = [s]
	ret = []
	for item in allcontent:
		ci = rawFromHTML(item)
		if len(ret) <= 10:
			cifilt = ''
			for sent in nltk.tokenize.sent_tokenize(ci):
				if (removeRedundant(onlyKeywordsIn(sent, syns)) or removeRedundant(onlyKeywordsIn(sent, scopes)) or getClassScore(query, sent) > 0):
					cifilt += sent + ' '
			if cifilt:
				ret.append('<p>'+cifilt.strip()+'</p>')
	return ''.join(ret)
#	return getInstancesOfRE(contentTagRE, s)

# returns true if string s contains any of the items in list l
def containsKeywords(s, l):
	for item in l:
		if item.lower().strip() in s.lower().strip() and len(item.lower().strip())>2:
			return True
	return False

# returns a list containing only those items from list l which are contained in string s
def onlyKeywordsIn(s, l):
	ret = []
	si = s.lower().strip()
	for item in l:
		ci = item.lower().strip()
		ind = si.find(ci)
		if (ind > -1 and ((ind == 0) or (not si[ind-1].isalpha()))) and not ci in ret and len(ci)>2:
			ret.append(ci)
	if 'course' in l and containsCourse(s):
		ret += getInstancesOfRE(courseRE, s)
	return ret

# returns a list containing only those items that occur in both list l1 and list l2
def inBoth(l1, l2):
	ret = []
	for item in l1:
		if item in l2:
			ret.append(item)
	return ret

# returns a list containing all the instances of each item in list l in string s
def getInstancesOf(l, s):
	ret = []
	toks = s.lower().split(' ')
	for tok in toks:
		for item in l:
			#if (len(item) > 3 and len(tok) <= len(item)+3 and item in tok) or item == tok:
			#if (len(item) > 3 and item in tok) or item == tok:
			if tok.startswith(item):
				ret.append(item)
				break
	#return removeRedundant(ret)
	return removeRepeats(ret)

########## class checks

# returns true if s contains patterns or words indicating a time class
def hasTime(s):
	feats = []

	if re.search(exactMTimeRE, s, re.I) or re.search(exactCTimeRE, s, re.I):
		feats.append('exact')
		feats.append('clock')
	if re.search(apprxTimeRE, s, re.I):
		feats.append('apprx')
		feats.append('clock')
	if re.search(dayRE, s, re.I):
		feats.append('weekday')
		feats.append('day')
	if re.search(fullDateRE, s, re.I):
		feats.append('date')
		feats.append('day')
	if re.search(condDateRE, s, re.I):
		feats.append('date')
		feats.append('day')
	if re.search(durationRE, s, re.I):
		feats.append('dur')

	if containsKeywords(s, generalTimeWords):
		if containsKeywords(s, pointTimeWords):
			feats.append('point')
		if containsKeywords(s, frequencyTimeWords):
			feats.append('freq')
		if containsKeywords(s, durationTimeWords):
			feats.append('dur')
		feats.append(getInstancesOf(generalTimeWords+pointTimeWords+frequencyTimeWords+durationTimeWords, s))
	else:
		feats.append(getInstancesOf(generalTimeWords, s))

	return removeRepeats(feats)

# returns true if s contains patterns or words indicating a contact class
def hasContactInfo(s):
	feats = []

	if re.search(phoneNumberRE, s, re.I):
		feats.append('phone')
		#feats.append('exact')
	if re.search(emailRE, s, re.I):
		feats.append('email')
		#feats.append('exact')
	if re.search(addressRE, s, re.I):
		feats.append('address')

#	emails = getInstancesOfRE(emailRE, s)
#	for i in range(0, len(emails)):
#		for item in ['(', ')', '[', ']', '{', '}']:
#			emails[i] = emails[i].replace(item, '')
#		toks = emails[i].split(' ')
#		for j in range(0, len(toks)):
#			if toks[j] == 'atsign' or toks[j] == 'at':
#				toks[j] = '@'
#			if toks[j] == 'dot':
#				toks[j] = '.'
#		emails[i] = ''.join(toks)
#	print(emails)

	if containsKeywords(s, emailContactWords):
		feats.append('email')
	if containsKeywords(s, phoneContactWords):
		feats.append('phone')
	feats.append(getInstancesOf(generalContactWords+emailContactWords+phoneContactWords, s))

	return removeRepeats(feats)
	#return feats

def hasLocation(s):
	feats = []

	if re.search(addressRE, s, re.I):
		feats.append('address')

	feats.append(getInstancesOf(generalLocationWords, s))

	return removeRepeats(feats)

def hasMoney(s):
	feats = []

	feats.append(getInstancesOf(generalMoneyWords, s))

	return removeRepeats(feats)

def hasPerson(s):
	feats = []

	feats.append(getInstancesOf(generalPersonWords, s))

	return removeRepeats(feats)

########## aggregate checks

# if a and b have stuff, calculate; if a has stuff but b doesn't, the score is zero; if a doesn't have stuff, the score is 1
def scoreFeatureSets(a, b):
	#if a[:-1] or a[-1]:
	if a != [[]]:
		score = 0.0
		#if b[:-1] or b[-1]:
		if b == [[]]:
			return score
		else:
			score += 1.0
			if a[:-1]:
				score += len(inBoth(a[:-1], b[:-1])) / len(a[:-1])
			else:
				score += 1.0
			if a[-1]:
				score += .5 * (len(inBoth(a[-1], b[-1])) / len(a[-1]))
			else:
				score += .5
			return (score / 2.5)
	else:
		return (1.0)

def getClassScore(q, r):
	num = 0
	den = 0

	htq = hasTime(q)
	hciq = hasContactInfo(q)
	hlq = hasLocation(q)
	hm = hasMoney(q)
	hp = hasPerson(q)

	if htq == [[]] and hciq == [[]] and hlq == [[]] and hm == [[]] and hp == [[]]:
		return -1
	else:
		if htq != [[]]:
			num += scoreFeatureSets(htq, hasTime(r))
			den += 1
		if hciq != [[]]:
			num += scoreFeatureSets(hciq, hasContactInfo(r))
			den += 1
		if hlq != [[]]:
			num += scoreFeatureSets(hlq, hasLocation(r))
			den += 1
		if hm != [[]]:
			num += scoreFeatureSets(hm, hasMoney(r))
			den += 1
		if hp != [[]]:
			num += scoreFeatureSets(hp, hasPerson(r))
			den += 1
		return (num / den)

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
#text = 'find me at 739 North High Street, Columbus, OH 43210'
#text = 'North High St South Campus Gateway Columbus Columbus, OH 43210'
#text = 'I was born on 5/11/2013'

#print(getInstancesOfRE(condDateRE, text.lower()))
#print(re.search(addressRE, text.lower(), re.I).group())

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
