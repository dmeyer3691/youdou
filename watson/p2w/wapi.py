### WATSON API CALLER (called in turn by rpr.py)

import requests
import base64
import json

########## initialize authentication input

baseurl	=	'https://watson-wdc01.ihost.com'
userid	=	'osu_student1'
passwd	=	'4bfyY9Y4'
authstr	=	userid + ":" + passwd
auth	=	'Basic ' + (base64.b64encode(bytes(authstr, 'utf-8'))).decode('utf-8')

### queries watson given query string; returns json dict
def queryWatson(query):

	########## initialize query-based (data) input

	data	=	{'question':{'questionText':query}}
	#data	=	{'question':{'questionText':query, 'formattedAnswer':True}}
	#data	=	{'question':{'questionText':query, 'formattedAnswer':'true'}}

	########## initialize url & header input

	#url		=	'https://watson-wdc01.ihost.com/instance/501/deepqa/v1/question'
	url		=	baseurl + '/instance/501/deepqa/v1/question'
	headers	=	{
					'Content-type'	:	'application/json',
					'Accept'		:	'application/json',
					'Authorization'	:	auth,
					'X-SyncTimeout'	:	'30'
				}

	########## post request

	r = requests.post(url, data=json.dumps(data), headers=headers)

	if r:
		#testPrint(r.json())
		return r.json()
	else:
		return {}

def getDocument(docurl):
	
	########## initialize url & header input

	url = baseurl + docurl
	headers	=	{'Authorization'	:	auth}

	r = requests.get(url, headers=headers)

	if r:
		return r.text
	else:
		return ''

### test by printing stuff (if called as main)
def testPrint(j):
	#q = 'classes about video games'
	#j = queryWatson(q)

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
		print('\tTEXT1:\t', 	j['question']['evidencelist'][i]['text'])
		#print('\tTEXT2:\t', 	j['question']['answers'][i]['text'])
		print('\tCONF:\t',		j['question']['answers'][i]['confidence'])

	print('\n----------\n')

########## only uncomment if calling directly

#testPrint()
#print(getDocument('/instance/501/deepqa/v1/question/document/PB_16CB6B0B3F0CF433F3816F94ABD0BA25/303/1066'))
#print(getDocument('/instance/501/deepqa/v1/question/document/T_4522AE0BF0879BE2E2ACCB7B58231BF7/0/-1'))
