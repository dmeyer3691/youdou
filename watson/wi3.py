### USAGE: python3 wi3.py

import requests
import base64
import json
#import nltk
from nltk import tokenize, grammar, parse

########## initialize query-based (data) input

query	=	'classes about video games'
data	=	{'question':{'questionText':query}}

########## initialize authentication input

userid	=	'osu_student1'
passwd	=	'4bfyY9Y4'
authstr	=	userid + ":" + passwd
auth	=	'Basic ' + (base64.b64encode(bytes(authstr, 'utf-8'))).decode('utf-8')

########## initialize url & header input

url		=	'https://watson-wdc01.ihost.com/instance/501/deepqa/v1/question'
headers	=	{
				'Content-type'	:	'application/json',
				'Accept'		:	'application/json',
				'Authorization'	:	auth,
				'X-SyncTimeout'	:	'30'
			}

########## post request

r = requests.post(url, data=json.dumps(data), headers=headers)
#print(json.dumps(r.json(), indent=4))

########## process and test print json

#j = json.loads(r.text)
j = r.json()
#print(j)

#print('KEYS:')
#for key in j['question']:
#	print('\t>>>\t', key)

print('\n----------QUERY INFO----------\n')

if 'questionText' in j['question']:
	print('QUERY:\t\t',		j['question']['questionText'])
if 'latlist' in j['question']:
	print('LATLIST:\t',		j['question']['latlist'])
if 'focuslist' in j['question']:
	print('FOCUSLIST:\t',	j['question']['focuslist'])
if 'qclasslist' in j['question']:
	print('CLASSLIST:\t',	j['question']['qclasslist'])

print('\n----------ANSWER INFO----------\n')

for i in range(0, len(j['question']['answers'])):
	print('\nTITLE:\t', 	j['question']['evidencelist'][i]['title'])
	print('\tTEXT1:\t', 	tokenize.sent_tokenize(j['question']['evidencelist'][i]['text']))
	#print('\tTEXT2:\t',		tokenize.sent_tokenize(j['question']['answers'][i]['text']))
	print('\tCONF:\t',		j['question']['answers'][i]['confidence'])

print('\n----------\n')

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
				'content'	: j['question']['evidencelist'][i]['text'],
				'also'		: also
			}
	results.append(dic)

ret =	{
			'title'		: title,
			'blurb'		: blurb,
			'results'	: results
		}

print(json.dumps(ret, indent=4))
