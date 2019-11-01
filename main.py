import requests
import json

myToken = 'ecc69723-9515-4a86-a91a-b370e7a9e369'
# myUrl = 'https://api.navitia.io/v1/coverage'
myUrl = 'https://api.navitia.io/v1/coverage/fr-idf/pt_objects?q=metro'

head = {'Authorization': myToken}
response = requests.get(myUrl, headers=head)

print(response.status_code)

data = response.json()
# print data['pt_objects'][0]['name']

for element in data['pt_objects']:
    print(element['name'])

print("\n")
# print len(data['pt_objects'][3])

for obj in data['pt_objects']:
    if 'line' in obj:
        print(obj['line']['name'])

print("\n")
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