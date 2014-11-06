import requests
import json
url = "https://watson-wdc01.ihost.com/instance/501/deepqa/v1/question"
data = {'question': { 'questionText': 'What is depression?' }}
headers = {'Content-type': 'application/json', 'Accept': 'application/json', 'Authorization': 'Basic b3N1X3N0dWRlbnQxOjRiZnlZOVk0', 'X-SyncTimeout': '30'}
r = requests.post(url, data=json.dumps(data), headers=headers)

print (r.status_code)
print(r.json())
print(r.raw)
