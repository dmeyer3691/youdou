### USAGE: python3 rpr.py

import sys
sys.path.append('/app/app/controllers')
import wapi, nlp
import json

########## get watson's stuff

query = sys.argv[1]
j = wapi.queryWatson(query)

########## initialize

storedInterests = ['animation', 'board games']
currentEvents = [{'name' : 'LAN PARTY', 'description' : 'Come play video games and eat Cheetos all night!', 'date' : 'November 18, 2014'}, {'name' : 'Cat Fanclub Meeting', 'description' : 'Our bimonthly meeting all about our favorite pets.', 'date' : 'November 12, 2014'}]
cheapAsFree = [{'name' : 'GameStop BOGO', 'keywords' : ['video games', 'computer games'], 'description' : 'Say the code "You Do U is awesome" at the GameStop south of campus to buy one game and get another free!'}, {'name' : '50% off the special You Do U roll', 'keywords' : ['sushi', 'roll', 'japanese', 'food', 'asian', 'restaurant'], 'description' : 'Come to Fusian sometime between now and Saturday to get half-off on our limited time only special You Do U roll!'}]

title = 'Q: ' + query

kws = nlp.nps(query)
syns = nlp.addSyns(kws)
scopesyns = nlp.relevantScopes(query)

#print(kws)
#print(syns)
#print(scopesyns)

########## get relevant events and offers

events = []
offers = []

for event in currentEvents:
	fullEvent = event['name'].strip()+' '+event['description'].strip()
	relevantTo = nlp.removeRedundant(nlp.onlyKeywordsIn(fullEvent, syns))
	if relevantTo:
		event['relevantTo'] = relevantTo
		alsolist = []
		for item in storedInterests:
			if item in fullEvent:
				alsolist.append(item)
		also = alsolist
		event['also'] = also
		events.append(event)

for offer in cheapAsFree:
	fullOffer = offer['name'].strip()+' '+(' '.join(offer['keywords'])).strip()+' '+offer['description'].strip()
	relevantTo = nlp.removeRedundant(nlp.onlyKeywordsIn(fullOffer, syns))
	if relevantTo:
		offer['relevantTo'] = relevantTo
		alsolist = []
		for item in storedInterests:
			if item in fullOffer:
				alsolist.append(item)
		also = alsolist
		offer['also'] = also
		offers.append(offer)

########## sort out watson's results

recommendedResults = []
possibleResults = []

if j and 'evidencelist' in j['question']:

	title = 'Q: ' + j['question']['questionText']

	docs = []

	for i in range(0, len(j['question']['evidencelist'])):
	#for i in range(0, len(j['question']['answers'])):
		heading = j['question']['evidencelist'][i]['title'].strip()
		if ' : ' in heading:
			sep = nlp.removeRepeats(heading.split(' : ')[1:])
			heading = ' | '.join(sep).strip()
		if heading.startswith("SH SR "):
			heading = heading[6:]

		content = j['question']['evidencelist'][i]['text'].strip()
		fullAnswer = heading + ' ' + content

		'''TODO: weight importance of keywords by length? so long shared things are better than short shared things?'''
		headingKW = nlp.removeRedundant(nlp.onlyKeywordsIn(heading, syns))
		contentKW = nlp.removeRedundant(nlp.onlyKeywordsIn(content, syns))
		relevantTo = nlp.removeRedundant(nlp.onlyKeywordsIn(fullAnswer, syns))
#		relevantTo = nlp.removeRedundant(headingKW+contentKW)

		headingScopes = nlp.removeRedundant(nlp.onlyKeywordsIn(heading, scopesyns))
		contentScopes = nlp.removeRedundant(nlp.onlyKeywordsIn(content, scopesyns))
		relevantScopes = nlp.removeRedundant(nlp.onlyKeywordsIn(fullAnswer, scopesyns))

		alsolist = []
		for item in storedInterests:
			if item in fullAnswer and not item in relevantTo:
				alsolist.append(item)
		also = alsolist

		#print(fullAnswer)
		#print('>>>', nlp.getClassScore(query, fullAnswer))
		#print('>>>', nlp.getScopeScore(query, fullAnswer))

		doc = j['question']['evidencelist'][i]['document'].strip()
		adjdoc = '/'.join(doc.split('/')[:-2]+['0','-1'])
		content = nlp.removeStuffFromHTML(wapi.getDocument(adjdoc))
		actuallen = len(nlp.rawFromHTML(content))
		if 20 < actuallen < 10000 and len(heading) < 500 and not '.....' in content and not '__' in content and not '__' in heading and not 'table of contents' in heading and not doc in docs and ((relevantTo) or (not syns and relevantScopes)):
			docs.append(adjdoc)

			snip = nlp.getContentHTML(content, syns, scopesyns, query)

			dic =	{	
						'title'			: heading,
						'snippet'		: snip,
						'content'		: content,
						'relevantTo'	: nlp.removeRedundant(relevantTo+relevantScopes),
						'also'			: also,
						'document'		: adjdoc
					}

			topicInHeading = (len(headingKW) > 0)
			#scopeInHeading = (nlp.getScopeScore(query, heading) != 0)
			#scopeInHeading = (len(scopesyns) == 0 or len(headingScopes) > 0)
			scopeInHeading = (len(headingScopes) > 0)
			classInHeading = (nlp.getClassScore(query, heading) != 0)

			topicInContent = (len(contentKW) > 0)
			#scopeInContent = (nlp.getScopeScore(query, content) != 0)
			#scopeInContent = (len(scopesyns) == 0 or len(contentScopes) > 0)
			scopeInContent = (len(contentScopes) > 0)
			classInContent = (nlp.getClassScore(query, content) != 0)

			enoughscopes = (nlp.countScopeTypes(relevantScopes) >= nlp.countScopeTypes(scopesyns) - 1)

			if len(scopesyns) == 0:
				if topicInHeading or topicInContent:
					if snip and (classInHeading or classInContent):
						recommendedResults.append(dic)
					else:
						possibleResults.append(dic)
			else:
				#if (topicInHeading and topicInContent and (scopeInHeading or scopeInContent) and (classInHeading or classInContent)):
				if snip and ((topicInHeading or topicInContent) and (scopeInHeading or scopeInContent) and enoughscopes and (classInHeading or classInContent)):
					recommendedResults.append(dic)
				elif (topicInHeading or topicInContent) and (scopeInHeading or scopeInContent or classInHeading or classInContent):
					possibleResults.append(dic)

########## set the blurb

blurb = ''
if (recommendedResults or possibleResults):
	blurb = 'Here are some resources you might look into.'
elif j:
	if (events or offers):
		blurb = 'Watson doesn\'t seem to have anything matching your search. Here are some other opportunities that may interest you.'
	else:
		blurb = 'There doesn\'t seem to be anything matching your search. Try adjusting your query and ask again.'
else:
	if (events or offers):
		blurb = 'Watson doesn\'t seem to be working at the moment. Here are some opportunities that might interest you in the meantime.'
	else:
		blurb = 'There seems to be something wrong with Watson. Please try again later.'

########## RETURN OF THE JEDI--I MEAN JSON

ret =	{
			'title'		: title,
			'blurb'		: blurb,
			'results'	:	{
								'recommended'	: recommendedResults,
								'possible'		: possibleResults
							},
			'events'	: events,
			'offers'	: offers
		}

print(json.dumps(ret, indent=4))
#with open('exampleJSON.txt', 'w') as outfile:
#	outfile.write(json.dumps(ret, outfile, indent=4))
