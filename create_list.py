import sys
import requests
import json

myToken = '5156beb5-3feb-4866-8ac5-039143adb326'
myStart = sys.argv[1]
myFinish = sys.argv[2]
myUrl = 'https://api.navitia.io/v1/coverage/fr-idf/physical_modes/physical_mode:Metro/lines'
head = {'Authorization': myToken}
response = requests.get(myUrl, headers=head)
data = response.json()

lines = [{}] * 16

routes = []

for i in range(0, 16):
    for obj in data['lines'][i]['routes']:
        routes.append(obj['id'])
        break

j = 0

for i in routes:
    myUrl = 'https://api.navitia.io/v1/coverage/fr-idf/routes/' + i + '?depth=3'

    head = {'Authorization': myToken}
    response = requests.get(myUrl, headers=head)

    data = response.json()
    all_stops = {}
    for obj in data['routes'][0]['stop_points']:
        label = json.dumps(obj['label'])
        stop_id = json.dumps(obj['stop_area']['id'])
        all_stops[stop_id.replace('\"', '')] = [label.replace('\"', ''), i]
    lines[j] = all_stops
    j += 1