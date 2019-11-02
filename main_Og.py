import sys
import colors as col
import requests
import json
import check_input as ch_in

ch_in.initial_check()

myToken = '5156beb5-3feb-4866-8ac5-039143adb326'
myStart = sys.argv[1]
myFinish = sys.argv[2]
myUrl = 'https://api.navitia.io/v1/coverage/fr-idf/physical_modes/physical_mode:Metro/lines'
head = {'Authorization': myToken}
response = requests.get(myUrl, headers=head)
data = response.json()
routes = []

for i in range(0, 16):
    for obj in data['lines'][i]['routes']:
        routes.append(obj['id'])
        break

list = []

for i in routes:
    myUrl = 'https://api.navitia.io/v1/coverage/fr-idf/routes/' + i + '?depth=3'

    head = {'Authorization': myToken}
    response = requests.get(myUrl, headers=head)

    data = response.json()

    for obj in data['routes'][0]['stop_points']:
        label = json.dumps(obj['label'])
        stop_id = json.dumps(obj['stop_area']['id'])
        if (label not in list):
            list.append(label)
            list.append(stop_id.replace('\"', ''))

start = ch_in.check_Start(list)
finish = ch_in.check_Finish(list)

if len(start) < 1 or len(finish) < 1:
    sys.exit(col.RED + "\nWe haven't found any corresponding Metro Stations try again!\nUsage: ./ratp [Start station] [Finish Station]\n" + col.RESET)
print("Which Starting station do you want to use?")
for elem in start:
    print (str(start.index(elem)) + '. ' + elem)
choice = -1
while choice < 0 or choice >= len(start):
    choice = int(input("Choose: "))
Str = start[choice]
for elem in finish:
    print (str(finish.index(elem)) + '. ' + elem)
choice = -1
while choice < 0 or choice >= len(finish):
    choice = int(input("Choose: "))
Fns = finish[choice]
print(Str)
print(Fns)

def get_stop_area(station, list):
	for element in list:
		if station == element:
			return (list[list.index(element) + 1])

strtArea = get_stop_area(Str, list)
arivArea = get_stop_area(Fns, list)

# myUrl = 'https://api.navitia.io/v1/coverage/fr-idf/stop_areas/stop_area:0:SA:59238/physical_modes/physical_mode%3AMetro/departures?'
myUrl = 'https://api.navitia.io/v1/coverage/fr-idf/stop_areas/' + strtArea + '/physical_modes/physical_mode%3AMetro/departures?'
print (myUrl)
head = {'Authorization': myToken}
response = requests.get(myUrl, headers=head)

data = response.json()

print(col.YELLOW + "\nDepartures from\n" + Str + col.RESET)
for obj in data['departures']:
    #if 'line' in obj:
    # for obj1 in obj['line']['routes']:
    depTime = (obj['stop_date_time']['base_departure_date_time'])
    depTime = depTime[9:-4] + ':'+ depTime[11:-2]
    print (depTime + '\t' + (obj)['route']['direction']['name'])

9 - 12
# print (list)