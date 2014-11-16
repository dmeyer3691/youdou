### USAGE: python3 rpr.py

import sys
sys.path.append('/app/app/controllers')
import wapi, kw, nlp
import json
#import nltk

########## get watson's stuff

#query = 'classes about video games'
#query = 'how can i contact health services'
#query = 'when is health services open'
#query = 'groups that involve board games and video games'
#query = 'clubs about cats'
#query = 'computer science scholarships'
query = sys.argv[1]
j = wapi.queryWatson(query)

########## do the magic

if j:

	#interest = 'video games'
	storedInterests = ['animation', 'board games']
	currentEvents = [{'name' : 'LAN PARTY!!!', 'description' : 'Come play video games and eat Cheetos all fukken night!', 'date' : 'November 18, 2014'}, {'name' : 'Cat Fanclub Meeting', 'description' : 'Our bimonthly meeting all about our favorite pets.', 'date' : 'November 12, 2014'}]

	title = 'Q: ' + j['question']['questionText']
	#blurb = 'Here are some resources you might look into based on your interest in ' + interest + '.'
	blurb = 'Here are some resources you might look into.'

	kws = nlp.nps(query)
	syns = nlp.addSyns(kws)

	#print(kws)
	#print(syns)

	recommendedResults = []
	possibleResults = []
	otherResults = []
	for i in range(0, len(j['question']['answers'])):
		fullAnswer = j['question']['evidencelist'][i]['title'].strip() + ' ' + j['question']['evidencelist'][i]['text'].strip()

		'''TODO: weight importance of keywords by length? so long shared things are better than short shared things?'''
		'''ALSOTODO: extract interests...adjectivish sometimes?  i.e., anime club meetings'''
		relevantTo = nlp.removeRedundant(kw.onlyKeywordsIn(fullAnswer, syns))

		alsolist = []
		for item in storedInterests:
			if item in fullAnswer and not item in relevantTo:
				alsolist.append(item)
		#also = ', '.join(alsolist)
		also = alsolist

		#print(fullAnswer)
		#print('>>>', kw.getClassScore(query, fullAnswer))
		#print('>>>', kw.getScopeScore(query, fullAnswer))

		dic =	{	
					'entity'		: j['question']['evidencelist'][i]['title'],
					'title'			: j['question']['evidencelist'][i]['title'],
					'content'		: j['question']['evidencelist'][i]['text'],
					#'content'		: nltk.tokenize.sent_tokenize(j['question']['evidencelist'][i]['text']),
					'relevantTo'	: relevantTo,
					'also'			: also
				}

		confidence = float(j['question']['answers'][i]['confidence'])
		#answersQuestionBool = kw.answersQuestion(query, fullAnswer)
		answersQuestionBool = (kw.getClassScore(query, fullAnswer) != 0 and kw.getScopeScore(query, fullAnswer) != 0)
		if (answersQuestionBool and len(relevantTo) >= min(len(kws), 2)) or confidence > .9:
			recommendedResults.append(dic)
		#elif (answersQuestionBool or relevantTo) or confidence > .2:
		elif relevantTo or confidence > .2:
			possibleResults.append(dic)
		else:
			otherResults.append(dic)

	events = []
	for event in currentEvents:
		fullEvent = event['name'].strip()+' '+event['description'].strip()
		relevantTo = nlp.removeRedundant(kw.onlyKeywordsIn(fullEvent, syns))
		if relevantTo:
			event['relevantTo'] = relevantTo
			alsolist = []
			for item in storedInterests:
				if item in fullEvent:
					alsolist.appent(item)
			#also = ', '.join(alsolist)
			also = alsolist
			event['also'] = also
			events.append(event)

	ret =	{
				'title'		: title,
				'blurb'		: blurb,
				'results'	:	{
									'recommended'	: recommendedResults,
									'possible'		: possibleResults,
									'other'			: otherResults
								},
				'events'	: events
			}

	print(json.dumps(ret, indent=4))
	#with open('exampleJSON.txt', 'w') as outfile:
	#	outfile.write(json.dumps(ret, outfile, indent=4))

else:
	print(json.dumps({}, indent=4))
