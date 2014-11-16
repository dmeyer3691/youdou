### USAGE: python3 nlp.py

import re
import nlp

########## REs

##### domain/scope REs
## academic
courseRE = r'[A-Z]{3,4}[\s-]?[0-9]{3,4}'

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
#addressRE = r''

########## lexicons

##### domain/scope lexicons
## academic
generalAcademicWords = ['undergraduate', 'graduate', 'undergrad', 'grad']
courseAcademicWords = ['course', 'class', 'requirement', 'credit']
focusAcademicWords = ['major', 'minor', 'focus', 'field', 'degree', 'bachelor', 'master', 'phd', 'doctorate', 'doctoral']
researchAcademicWords = []
moneyAcademicWords = ['scholarship', 'fellowship', 'award', 'fund']
## social
generalSocialWords = ['group', 'club', 'organization', 'play', 'fun']

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

# returns true if string s contains any of the items in list l
def containsKeywords(s, l):
	for item in l:
		if item.lower().strip() in s.lower().strip() and len(item.lower().strip())>2:
			return True
	return False

# returns a list containing only those items from list l which are contained in string s
def onlyKeywordsIn(s, l):
	ret = []
	for item in l:
		if item.lower().strip() in s.lower().strip() and not item.lower().strip() in ret and len(item.strip())>2:
			ret.append(item.lower().strip())
	return ret

# returns a list containing only those items that occur in both list l1 and list l2
def inBoth(l1, l2):
	ret = []
	for item in l1:
		if item in l2:
			ret.append(item)
	return ret

# returns a list containing all the instances of pattern p in string s
def getInstancesOfRE(p, s):
	ret = []
	s2 = s
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

# returns a list containing all the instances of each item in list l in list s
def getInstancesOf(l, s):
	ret = []
	toks = s.split(' ')
	for tok in toks:
		for item in l:
			#if (len(item) > 3 and len(tok) <= len(item)+3 and item in tok) or item == tok:
			if (len(item) > 3 and item in tok) or item == tok:
				ret.append(tok)
				ret.append(item)
				break
	#return nlp.removeRedundant(ret)
	return nlp.removeRepeats(ret)

########## domain/scope checks

# returns true if string s contains patterns or words indicating an academic topic
def hasAcademics(s):
	feats = []

	if re.search(courseRE, s):
		feats.append('course')

	if containsKeywords(s, courseAcademicWords):
		feats.append('course')
	if containsKeywords(s, focusAcademicWords):
		feats.append('focus')

	feats.append(getInstancesOf(generalAcademicWords+courseAcademicWords+focusAcademicWords+moneyAcademicWords, s))

	return nlp.removeRepeats(feats)

# returns true if s contains patterns or words indicating a social domain
def hasSocial(s):
	feats = []

	feats.append(getInstancesOf(generalSocialWords, s))

	return nlp.removeRepeats(feats)

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

	feats.append(getInstancesOf(generalLocationWords, s))

	return nlp.removeRepeats(feats)

########## aggregate checks

# if a and b have stuff, calculate; if a has stuff but b doesn't, the score is zero; if a doesn't have stuff, the score is 1
def scoreFeatureSets(a, b):
	#if a[:-1] or a[-1]:
	if a != [[]]:
		score = 0.0
		#if b[:-1] or b[-1]:
		if b != [[]]:
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

def getScopeScore(q, r):
	num = 0
	den = 0

	num += scoreFeatureSets(hasAcademics(q), hasAcademics(r))
	den += 1

	num += scoreFeatureSets(hasSocial(q), hasSocial(r))
	den += 1

	return (num / den)

def getClassScore(q, r):
	num = 0
	den = 0

	num += scoreFeatureSets(hasTime(q), hasTime(r))
	den += 1

	num += scoreFeatureSets(hasContactInfo(q), hasContactInfo(r))
	den += 1

	num += scoreFeatureSets(hasLocation(q), hasLocation(r))
	den += 1

	return (num / den)

# returns the item in l that gets the maximum feature similarity score relative to s
def maxScored(s, l):
	scores = [((getScopeScore(s, item)+getClassScore(s, item))/2) for item in l]
	#scores = [getClassScore(s, item) for item in l]
	return l[(max(enumerate(scores))[0])]

def answersQuestion(q, r):
	ret = False
	qclasses = nlp.getQClass(q)
	if hasAcademics(q) != [[]]:
		if hasAcademics(r) != [[]]:
			ret = True
	if hasSocial(q) != [[]]:
		if hasSocial(r) != [[]]:
			ret = True
	if hasTime(q) != [[]] or 'TIM' in qclasses:
		if hasTime(r) != [[]]:
			ret = True
	if hasContactInfo(q) != [[]]:
		if hasContactInfo(r) != [[]]:
			ret = True
	if hasLocation(q) != [[]] or 'LOC' in qclasses:
		if hasLocation(r) != [[]]:
			ret = True
	return ret

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
#print(maxScored(text1, text2))
#print(hasContactInfo(text2))
#print(getInstancesOfRE(phoneNumberRE, text2))
#if re.search(phoneNumberRE, text2, re.I):
#	print('phone')

#temp = hasAcademics(text)
#temp = hasAcademics(text)
#if temp:
#	print(temp)
#temp = hasContactInfo(text)
#if temp:
#	print(temp)
