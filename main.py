import requests
import json
import colors as col

myToken = 'ecc69723-9515-4a86-a91a-b370e7a9e369'
# myUrl = 'https://api.navitia.io/v1/coverage'
# myUrl = 'https://api.navitia.io/v1/coverage/fr-idf/pt_objects?q=RATP'
myUrl = 'https://api.navitia.io/v1/coverage/fr-idf/pt_objects?q=metro'

head = {'Authorization': myToken}
response = requests.get(myUrl, headers=head)

print(col.YELLOW + "Response Status Code : " + col.RESET)
print(response.status_code)

data = response.json()
# print data['pt_objects'][0]['name']

print(col.YELLOW + "\nMetro Line Names\n" + col.RESET)
for element in data['pt_objects'][3:]:
    print(element['name'])

# print len(data['pt_objects'][3])
print(col.YELLOW + "\nMetro Line - Terminus Names\n" + col.RESET)
for obj in data['pt_objects']:
    if 'line' in obj:
        print(obj['line']['name'])
        
print(col.YELLOW + "\nMetro Stop Areas of Lines\n" + col.RESET)
for obj in data['pt_objects']:
    if 'line' in obj:
        for obj1 in obj['line']['routes']:
            print(obj1['direction']['stop_area']['label'])

# for element in data['pt_objects']:
# #    print("Key: " + k)
# #    print("Value: " + str(v))
#    print data['pt_objects'][index]['line']['name']

# for element in data['pt_objects']:
#     print(element['network'])

# def jprint(obj):
#     # create a formatted string of the Python JSON object
#     text = json.dumps(obj, sort_keys=True, indent=4)
#     print(text)

# jprint(response.json())