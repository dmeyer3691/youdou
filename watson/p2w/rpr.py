### USAGE: python3 wi3.py

import wapi
import json
#import nltk
from nltk import tokenize, grammar, parse, chunk, pos_tag

########## get watson's stuff

#query = 'classes about video games'
query = 'how can i contact health services'
j = wapi.queryWatson(query)

########## do the magic

interest = 'video games'
interests = ['animation', 'board games']

title = 'Q: ' + j['question']['questionText']
blurb = 'Here are some resources you might look into based on your interest in ' + interest + '.'

results = []
for i in range(0, len(j['question']['answers'])):
	alsolist = []
	for item in interests:
		if item in j['question']['evidencelist'][i]['title'] or item in j['question']['evidencelist'][i]['text']:
			alsolist.append(item)
	also = ', '.join(alsolist)

	dic =	{	
				'entity'	: j['question']['evidencelist'][i]['title'],
				'title'		: j['question']['evidencelist'][i]['title'],
				#'content'	: j['question']['evidencelist'][i]['text'],
				'content'	: tokenize.sent_tokenize(j['question']['evidencelist'][i]['text']),
				'also'		: also
			}
	results.append(dic)

ret =	{
			'title'		: title,
			'blurb'		: blurb,
			'results'	: results
		}

print(json.dumps(ret, indent=4))

#sents = tokenize.sent_tokenize(j['question']['evidencelist'][0]['text'])
sents = tokenize.sent_tokenize(query)
chunks = [chunk.ne_chunk(pos_tag(tokenize.word_tokenize(s))) for s in sents]

entities = []
for chunk in chunks[0][2]:
	if chunk != '':
		item = chunk
		entities.append(item)

print(chunks)
#print(entities)
