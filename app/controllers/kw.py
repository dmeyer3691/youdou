### USAGE: python3 nlp.py

import re
import nlp

########## REs

courseRE = r'[A-Z]{3,4}[\s-]?[0-9]{3,4}'

titleTagRE = r'(<head>.*?</head>)|(<h1.*>.*?</h1>)|(<span>.*?</span>)'
contentTagRE = r'(<p>.*?</p>)|(<tr(\s?)>.*?</tr>)|(<li>.*?</li>)'
anyTagRE = r'(<.+?>)'

##### class REs
## time
exactMTimeRE = r'((([2][0-3])|([0-1]?[0-9]))((:[0-5][0-9])|\so\'clock))|(((([2][0-3])|([0-1][0-9]))((:)?[0-5][0-9]))((\s)hours))'
exactCTimeRE = r'((([1][0-2])|([0]?[0-9]))(:[0-5][0-9])?)(((\s?)o\'clock)|((\s?)[ap](\.)?(m)(\.)?)){1,2}'
apprxTimeRE = r'((at|exactly|around|about|before|after)(\s))?(((a)(\s))?((five|ten|quarter|half)(\s))((til|\'til|until|to|after|past)(\s)))?(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|noon|midnight)((\s)o\'clock)?((\s)[ap](\.)?(m)(\.)?)?'
dayRE = r'((on|each|every|every(\s)other)(\s))?((\w)*((day(s?))|morrow))'
#ADateRE = r'(()|())'
#EDateRE = r''
durationRE = r'([0-9]+|(one|two|three|four|five|six|seven|eight|nine|ten)(\s)(second(s?)|minute(s?)|hour(s?)|day(s?)|week(s?)|month(s?)|year(s?)|quarter(s?)|semester(s?)|season(s?))'
waitRE = r'(in|for|after)?((NUMERIC)|(ALPHANUM)|(APPRX))(second(s?)|minutes(s?)|hour(s?)|week(s?)|month(s?)|year(s?)|quarter(s?)|semester(s?)|season(s?))'
NNumberRE = r'([0-9]{1,3}(,?))?([0-9]{3}(,?))?([0-9]{1-3})?((\.)[0-9]+)?'
ANumberRE = r'zero|(((((((twen|thir|for|fif|six|seven|eigh|nine)(ty)(-?))?(one|two|three|four|five|six|seven|eight|nine)?)|ten|eleven|twelve|((thir|four|fif|six|seven|eigh|nine)(teen)))((\s)(point)(zero|one|two|three|four|five|six|seven|eight|nine)+)?)?(hundred|thousand|([a-z]+(illion))((\s)|(and\s)|(,\s))?))*(((((twen|thir|for|fif|six|seven|eigh|nine)(ty)(-?))?(one|two|three|four|five|six|seven|eight|nine)?)|ten|eleven|twelve|((thir|four|fif|six|seven|eigh|nine)(teen)))((\s)(point|and)(zero|one|two|three|four|five|six|seven|eight|nine)+)?))'
## contact
phoneNumberRE = r'(\+?)(([0-9]([\s\.-]?))?((\(?)[0-9]{3}(\)?)([\s\.-]?)))?([0-9]{3}([\s\.-]?))([0-9]{4})'
emailRE = r'([\(\[\{]\s*)*(\S+)(\s*[\)\]\}])*((\s*)(\.|(([\(\[\{]\s*)*dot([\)\]\}]\s*)*))(\s*)([\(\[\{]\s*)*(\S+)(\s*[\)\]\}])*(\s*))*(\s*)(@|(([\(\[\{]\s*)*at(sign)?([\)\]\}]\s*)*))((\s*)([\(\[\{]\s*)*(\S+)(\s*[\)\]\}])*(\s*)(\.|(([\(\[\{]\s*)*dot([\)\]\}]\s*)*)))+(\s*)([\(\[\{]\s*)*(com|edu|gov|me|info|co|net)(\s*[\)\]\}])*'
addressRE = r'([0-9]+(/s+))?([a-z]+(/s+)){1,2}((ave|avenue|ct|court|dr|drive|ln|lane|pkwy|parkway|rd|road|st|street|way)(\.?)((\s+)[NSEW])?)?(,(/s)*)?(([a-z]+(\s+)){1,2},(/s+)[a-z](/s+))[0-9]{5}(-[0-9]{4})?'

########## lexicons

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
generalLocationWords = ['where', 'location', 'located', 'place', 'building', 'center', 'room', 'library', 'office', 'house', 'department']
## money
generalMoneyWords = ['$', 'money', 'how much', 'dollar', 'cent', 'expensive', 'cheap', 'free', 'cost', 'loan', 'pay', 'paid', 'spend', 'spent', 'fee', 'charge']

########## general tools

# returns html sans titleish thing
def removeStuffFromHTML(s):
	return re.compile(titleTagRE).sub('', s).strip()

def rawFromHTML(s):
	return ' '.join(re.compile(anyTagRE).sub(' ', s).split()).strip()

def getContentHTML(s, syns, scopes, query):
	allcontent = nlp.getInstancesOfRE(contentTagRE, s)
	ret = []
	for item in allcontent:
		if nlp.removeRedundant(onlyKeywordsIn(item, syns)) or nlp.removeRedundant(onlyKeywordsIn(item, scopes)) or getClassScore(query, item) > 0:
			#ret.append(item)
			ret.append('<p>'+rawFromHTML(item)+'</p>')
	return ''.join(ret)
#	return nlp.getInstancesOfRE(contentTagRE, s)

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
	if 'course' in l and nlp.containsCourse(s):
		ret += nlp.getInstancesOfRE(courseRE, s)
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
	#return nlp.removeRedundant(ret)
	return nlp.removeRepeats(ret)

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
#	if re.search(dateRE, s, re.I):
#		feats.append('date')
#		feats.append('day')

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

	return nlp.removeRepeats(feats)

# returns true if s contains patterns or words indicating a contact class
def hasContactInfo(s):
	feats = []

	if re.search(phoneNumberRE, s, re.I):
		feats.append('phone')
		#feats.append('exact')
	if re.search(emailRE, s, re.I):
		feats.append('email')
		#feats.append('exact')
#	if re.search(addressRE, s, re.I):
#		feats.append('address')

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

	return nlp.removeRepeats(feats)
	#return feats

def hasLocation(s):
	feats = []

	if re.search(addressRE, s, re.I):
		feats.append('address')

	feats.append(getInstancesOf(generalLocationWords, s))

	return nlp.removeRepeats(feats)

def hasMoney(s):
	feats = []

	feats.append(getInstancesOf(generalMoneyWords, s))

	return nlp.removeRepeats(feats)

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

	if htq == [[]] and hciq == [[]] and hlq == [[]] and hm == [[]]:
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
		return (num / den)

##########
 
#text = 'where can i get training for a marathon'
#text = 'i made the girl a cake'
#text = 'the girl gave me some cake'
#text1 = 'what number can I call for a group to play video games'
#text = 'How can I contact health services?'
#text = 'clubs about cats'
#text = 'groups that are about video games and board games'
#text = 'groups that play video games, card games, and board games'
#text = 'I saw the man who stole my computer.'
#text = 'I like it, but that does not mean it\'s good'
#text = 'what time is LING5601'
#text = 'the courses are on Wednesdays at twelve PM.'
#text = 'you can reach me at 16144788550'
#text = 'you can reach me at [ azg ] ( atsign) {ling dot ohio-state} .edu'
#text1 = 'what days can i meet with ajda'
#text2 = ['you can reach me at [ azg ] ( atsign) {ling dot ohio-state} .edu or gokcen dot 2 @osu.edu.', 'I am usually around on Wednesdays but not on holidays. my office hours are between 3 and 5 pm.']

#text2 = ['Some of these activities could include things like playing video games together, watching movies or sports, engaging in card or board games or sharing hobbies or skills we have developed over the years.', 'This is not your traditional therapy group and we hope you can join us!', 'Please, call 614.292.5766, speak with your counselor or email Kipp for more information.']
#text2 = 'Please, call 614.292.5766, speak with your counselor or email Kipp for more information.'

#print(text1)
#print(hasContactInfo(text2))
#print(getInstancesOfRE(phoneNumberRE, text2))
#if re.search(phoneNumberRE, text2, re.I):
#	print('phone')

#if temp:
#	print(temp)
#temp = hasContactInfo(text)
#if temp:
#	print(temp)
