### USAGE: python3 nlp.py

import re
import nlp

##########

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
		if item.lower().strip() in s.lower().strip() and not item.lower().strip() in ret and len(item.lower().strip())>2:
			ret.append(item.lower().strip())
	return ret

# returns true if string s contains patterns or words indicating an academic topic
def hasAcademics(s):
	courseRE = r'[A-Z]{3,4}[\s-]?[0-9]{3,4}'

	courseWords = ['course', 'class', 'requirement', 'credit']
	focusWords = ['major', 'minor', 'focus', 'field', 'degree', 'undergraduate', 'graduate', 'undergrad', 'grad', 'bachelor', 'master', 'phd', 'doctorate', 'doctoral']
	moneyWords = ['scholarship', 'fellowship', 'award', 'fund']
	academicWords = courseWords + focusWords

	mentionsCourse = re.search(courseRE, s)
	
	return (mentionsCourse or containsKeywords(s, academicWords))

# returns true if string s contains patterns or words indicating a coursework topic
def hasCourse(s):
	courseRE = r'[A-Z]{3,4}[\s-]?[0-9]{3,4}'

	courseWords = ['course', 'class', 'requirement', 'credit']

	mentionsCourse = re.search(courseRE, s)
	
	return (mentionsCourse or containsKeywords(s, courseWords))

# returns true if s contains patterns or words indicating a social domain
def hasSocial(s):
	socialWords = ['group', 'club']

	return (containsKeywords(s, socialWords))

# returns true if s contains patterns or words indicating a time class
def hasTime(s):
	exactMTimeRE = r'((([2][0-3])|([0-1]?[0-9]))((:[0-5][0-9])|\so\'clock))|(((([2][0-3])|([0-1][0-9]))((:)?[0-5][0-9]))((\s)hours))'
	exactCTimeRE = r'((([1][0-2])|([0]?[0-9]))(:[0-5][0-9])?)(((\s?)o\'clock)|((\s?)[ap](\.)?(m)(\.)?)){1,2}'
	apprxTimeRE = r'((at|exactly|around|about|before|after)(\s))?(((a)(\s))?((five|ten|quarter|half)(\s))((til|\'til|until|to|after|past)(\s)))?(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|noon|midnight)((\s)o\'clock)?((\s)[ap](\.)?(m)(\.)?)?'

	dayRE = r'((on|each|every|every(\s)other)(\s))?((\w)+((day(s?))|morrow))'
	#ADateRE = r'(()|())'
	EDateRE = r''

	durationRE = r'([0-9]+|(one|two|three|four|five|six|seven|eight|nine|ten)(\s)(second(s?)|minute(s?)|hour(s?)|day(s?)|week(s?)|month(s?)|year(s?)|quarter(s?)|semester(s?)|season(s?))'
	waitRE = r'(in|for|after)?((NUMERIC)|(ALPHANUM)|(APPRX))(second(s?)|minutes(s?)|hour(s?)|week(s?)|month(s?)|year(s?)|quarter(s?)|semester(s?)|season(s?))'
	NNumberRE = r'([0-9]{1,3}(,?))?([0-9]{3}(,?))?([0-9]{1-3})?((\.)[0-9]+)?'
	ANumberRE = r'zero|(((((((twen|thir|for|fif|six|seven|eigh|nine)(ty)(-?))?(one|two|three|four|five|six|seven|eight|nine)?)|ten|eleven|twelve|((thir|four|fif|six|seven|eigh|nine)(teen)))((\s)(point)(zero|one|two|three|four|five|six|seven|eight|nine)+)?)?(hundred|thousand|([a-z]+(illion))((\s)|(and\s)|(,\s))?))*(((((twen|thir|for|fif|six|seven|eigh|nine)(ty)(-?))?(one|two|three|four|five|six|seven|eight|nine)?)|ten|eleven|twelve|((thir|four|fif|six|seven|eigh|nine)(teen)))((\s)(point|and)(zero|one|two|three|four|five|six|seven|eight|nine)+)?))'

	timeWords = ['when', 'schedule', 'hours', 'time', 'yearly', 'monthly', 'daily', 'hourly', 'semester', 'quarter']

	searchExactMTime = re.search(exactMTimeRE, s, re.I)
	searchExactCTime = re.search(exactCTimeRE, s, re.I)
	searchApprxTime = re.search(apprxTimeRE, s, re.I)

	searchDay = re.search(dayRE, s, re.I)
	#searchDate = re.search(dateRE, s, re.I)

	#print(searchExactMTime.group())
	#print(searchExactCTime.group())
	#print(searchApprxTime.group())
	#print(searchDay.group())

	mentionsTime = (searchExactMTime or searchExactCTime or searchApprxTime)
	#mentionsDay = (searchDay or searchDate)
	mentionsDay = (searchDay or False)

	return (mentionsTime or mentionsDay or containsKeywords(s, timeWords))

# returns true if s contains patterns or words indicating a contact class
def hasContactInfo(s):
	phoneNumberRE = r'(\+?)(([0-9]([\s-]?))?((\(?)[0-9]{3}(\)?)([\s-]?)))?([0-9]{3}([\s-]?))([0-9]{4})'
	emailRE = r'(\w+)(\s?)(@|([\(\[\{]at[\)\]\}]))((\s?)(\S+)(\s?)(\.|([\(\[\{]?dot[\)\]\}]?)))+(\s?)(com|edu|gov|me)'
	addressRE = r''

	contactWords = ['contact', 'reach', 'talk to', 'email', 'e-mail', 'phone', 'number', 'phone number', 'address', 'appointment']

	searchPhoneNumber = re.search(phoneNumberRE, s, re.I)
	searchEmail = re.search(emailRE, s, re.I)
	searchAddress = re.search(addressRE, s, re.I)

	#print(searchPhoneNumber.group())
	#print(searchEmail.group())

	#mentionsContactInfo = (searchPhoneNumber or searchEmail or searchAddress)
	mentionsContactInfo = (searchPhoneNumber or searchEmail)

	return (mentionsContactInfo or containsKeywords(s, contactWords))

def hasLocation(s):
	locationWords = ['where', 'location', 'located', 'place', 'building', 'center', 'room', 'library', 'office', 'house']

	return (containsKeywords(s, locationWords))

def answersQuestion(q, r):
	ret = False
	qclasses = nlp.getQClass(q)
	if hasAcademics(q):
		if hasAcademics(r):
			ret = True
	if hasCourse(q):
		if hasCourse(r):
			ret = True
	if hasSocial(q):
		if hasSocial(r):
			ret = True
	if hasTime(q) or 'TIM' in qclasses:
		if hasTime(r):
			ret = True
	if hasContactInfo(q):
		if hasContactInfo(r):
			ret = True
	if hasLocation(q) or 'LOC' in qclasses:
		if hasLocation(r):
			ret = True
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
#text = 'you can reach me at azg@ling.ohio-state.edu'

#if hasTime(text):
#	print('TIME!')
#if hasAcademics(text):
#	print('ACADEMICS!')
#if hasContactInfo(text):
#	print('CONTACT!')
