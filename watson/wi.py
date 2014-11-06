### Watson Interface
### USAGE: python3 wi/py

import urllib.request
from urllib.error import HTTPError
import base64
import json
#import urllib2

query = 'classes about video games'

url = 'https://watson-wdc01.ihost.com/instance/501/deepqa/v1/question'
userid = 'osu_student1'
passwd = '4bfyY9Y4'

req = urllib.request.Request(url)
auth = base64.b64encode(bytes(((userid + ":" + passwd).replace('\n', '')), 'utf-8'))
submtext = '{\"question\" : {\"questionText\":\"' + query + '\"}}'
subm = base64.b64encode(bytes(submtext, 'utf-8'))

req.add_header('Content-Type', 'application/json')
req.add_header('Accept', 'application/json')
req.add_header('X-SyncTimeout', '30')
req.add_header('Authorization', 'Basic ' + str(auth))

#ok = urllib.request.urlopen(req, urllib.urlencode(subm))
try:
	ok = urllib.request.urlopen(req, subm)
	print(ok.read())
except HTTPError as e:
	content = e.read()
	print(content)
