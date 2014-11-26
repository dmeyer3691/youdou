### USAGE: python3 rpr.py

import sys
sys.path.append('/app/app/controllers')
import wapi, kw, nlp
import json
#import nltk

########## get watson's stuff

query = sys.argv[1]
j = wapi.queryWatson(query)

########## do the magic

storedInterests = ['animation', 'board games']
currentEvents = [{'name' : 'LAN PARTY!!!', 'description' : 'Come play video games and eat Cheetos all fukken night!', 'date' : 'November 18, 2014'}, {'name' : 'Cat Fanclub Meeting', 'description' : 'Our bimonthly meeting all about our favorite pets.', 'date' : 'November 12, 2014'}]

title = 'Q: ' + query
blurb = 'There seems to be something wrong with Watson. Please try again later.'

recommendedResults = []
possibleResults = []
events = []

if j:

	title = 'Q: ' + j['question']['questionText']
	blurb = 'Here are some resources you might look into.'

	kws = nlp.nps(query)
	syns = nlp.addSyns(kws)

	scopesyns = nlp.relevantScopes(query)

	#print(kws)
	#print(syns)
	#print(scopesyns)

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
		headingKW = nlp.removeRedundant(kw.onlyKeywordsIn(heading, syns))
		contentKW = nlp.removeRedundant(kw.onlyKeywordsIn(content, syns))
		relevantTo = nlp.removeRedundant(kw.onlyKeywordsIn(fullAnswer, syns))
#		relevantTo = nlp.removeRedundant(headingKW+contentKW)

		headingScopes = nlp.removeRedundant(kw.onlyKeywordsIn(heading, scopesyns))
		contentScopes = nlp.removeRedundant(kw.onlyKeywordsIn(content, scopesyns))
		relevantScopes = nlp.removeRedundant(kw.onlyKeywordsIn(fullAnswer, scopesyns))

		alsolist = []
		for item in storedInterests:
			if item in fullAnswer and not item in relevantTo:
				alsolist.append(item)
		also = alsolist

		#print(fullAnswer)
		#print('>>>', kw.getClassScore(query, fullAnswer))
		#print('>>>', kw.getScopeScore(query, fullAnswer))

		doc = j['question']['evidencelist'][i]['document'].strip()
		adjdoc = '/'.join(doc.split('/')[:-2]+['0','-1'])
		content = kw.removeStuffFromHTML(wapi.getDocument(adjdoc))
		if 10 < len(content) < 10000 and len(heading) < 500 and not '__' in content and not doc in docs and ((relevantTo) or (not syns and relevantScopes)):
			docs.append(adjdoc)

			snip = kw.getContentHTML(content, syns, scopesyns, query)

			dic =	{	
						#'entity'		: heading,
						'title'			: heading,
						'snippet'		: snip,
						'content'		: content,
						#'content'		: nltk.tokenize.sent_tokenize(j['question']['evidencelist'][i]['text']),
						'relevantTo'	: relevantTo+relevantScopes,
						'also'			: also,
						'document'		: adjdoc
					}

			topicInHeading = (len(headingKW) > 0)
			#scopeInHeading = (kw.getScopeScore(query, heading) != 0)
			scopeInHeading = (len(scopesyns) == 0 or len(headingScopes) > 0)
			classInHeading = (kw.getClassScore(query, heading) != 0)

			topicInContent = (len(contentKW) > 0)
			#scopeInContent = (kw.getScopeScore(query, content) != 0)
			scopeInContent = (len(scopesyns) == 0 or len(contentScopes) > 0)
			classInContent = (kw.getClassScore(query, content) != 0)

			#if (topicInHeading and topicInContent and (scopeInHeading or scopeInContent) and (classInHeading or classInContent)):
			if ((topicInHeading or topicInContent) and (scopeInHeading or scopeInContent) and (classInHeading or classInContent)):
				recommendedResults.append(dic)
			elif (topicInHeading or topicInContent) and (scopeInHeading or scopeInContent or classInHeading or classInContent):
				possibleResults.append(dic)

	for event in currentEvents:
		fullEvent = event['name'].strip()+' '+event['description'].strip()
		relevantTo = nlp.removeRedundant(kw.onlyKeywordsIn(fullEvent, syns))
		if relevantTo:
			event['relevantTo'] = relevantTo
			alsolist = []
			for item in storedInterests:
				if item in fullEvent:
					alsolist.appent(item)
			also = alsolist
			event['also'] = also
			events.append(event)

ret =	{
			'title'		: title,
			'blurb'		: blurb,
			'results'	:	{
								'recommended'	: recommendedResults,
								'possible'		: possibleResults
							},
			'events'	: events
		}

print(json.dumps(ret, indent=4))
#with open('exampleJSON.txt', 'w') as outfile:
#	outfile.write(json.dumps(ret, outfile, indent=4))
