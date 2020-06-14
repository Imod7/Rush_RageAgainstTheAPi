import sys
import os
import colors as col
import requests
import json
import check_input as ch_in
import create_list

lines = create_list.lines

myToken = 'ecc69723-9515-4a86-a91a-b370e7a9e369'
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

for i in range(0, 16):
    myUrl = 'https://api.navitia.io/v1/coverage/fr-idf/routes/' + routes[i] + '?depth=3'

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
print(col.CYAN + "\nWhich Starting station do you want to use?\n" + col.RESET)
counter = 0
for elem in start:
    if "stop_area" not in elem: 
        print(col.BLUE + str(counter) + '. ' + elem.encode().decode('unicode-escape') + col.RESET)
        counter += 1
choice = -1
while choice < 0 or choice >= len(start):
    choice = input(col.RED + "Choose: " + col.RESET)
    if choice.isnumeric():
        choice = int(choice)
    else:
        choice = -1
Str = start[choice]
print(col.CYAN + "\nWhich Finish station do you want to use?\n" + col.RESET)
counter = 0
for elem in finish:
    if "stop_area" not in elem: 
        print(col.BLUE + str(counter) + '. ' + elem.encode().decode('unicode-escape') + col.RESET)
        counter += 1
choice = -1
while choice < 0 or choice >= len(finish):
    choice = input(col.RED + "Choose: " + col.RESET)
    if choice.isnumeric():
        choice = int(choice)
    else:
        choice = -1
Fns = finish[choice]
print(col.YELLOW + "\nYour chosen starting station is " + Str.encode().decode('unicode-escape') + col.RESET)
print(col.YELLOW + "Your chosen finish station is " + Fns.encode().decode('unicode-escape') + col.RESET)

def get_stop_area(station, list):
	for element in list:
		if station == element:
			return (list[list.index(element) + 1])

strtArea = get_stop_area(Str, list)
arivArea = get_stop_area(Fns, list)

if strtArea == arivArea:
    sys.exit(col.GREEN + "You're already there you silly!\n" + col.RESET)

myUrl = 'https://api.navitia.io/v1/coverage/fr-idf/stop_areas/' + strtArea + '/physical_modes/physical_mode%3AMetro/departures?'
head = {'Authorization': myToken}
response = requests.get(myUrl, headers=head)
data = response.json()

for obj in data ['departures']:
    if (obj)['route']['direction']['id'] == arivArea:
        depTime = (obj['stop_date_time']['base_departure_date_time'])
        depTime = depTime[9:-4] + ':'+ depTime[11:-2]
        print (depTime + '\t' + (obj)['route']['direction']['name'])


dest_lines = []
indices = []
counter = 0
for line in lines:
    if arivArea in line.keys():
        dest_lines.append(counter)
    counter += 1
output = [strtArea]


def rule3(current_line):
    location = False
    finished = False
    if current_line != 0:

        counter = 0
        for station in hub[0]:
            if station == strtArea:
                location = True
            if location == True:
                if station in lines[1]:
                    finished = True
                    hub[0] = lines[1]
                    if station != strtArea:
                        output.append(station)
                        indices.append(1)
                        return
                if station in lines[6]:
                    finished = True
                    hub[0] = lines[6]
                    if station != strtArea:
                        output.append(station)
                        indices.append(6)
                        return
            counter += 1

        if finished == False:
            location = False
            counter = 0
            for station in hub[0][::-1]:
                if station == strtArea:
                    location = True
                if location == True:
                    if station in lines[1]:
                        finished = True
                        hub[0] = lines[1]
                        if station != strtArea:
                            output.append(station)
                            indices.append(1)
                            return
                    if station in lines[6]:
                        finished = True
                        hub[0] = lines[6]
                        if station != strtArea:
                            output.append(station)
                            indices.append(6)
                            return
                counter += 1


def rule4():
    for station in hub[0]:
        for i in dest_lines:
            if station in lines[i]:
                if station not in output:
                    output.append(station)
                    indices.append(i)
                return
current_line = 0

hub = []
counter = 0
for line in lines:
    if strtArea in line.keys():
        hub.append(line)
        indices.append(counter)
        if arivArea in line.keys():
            break
        else:
            rule3(current_line)
            rule4()
            break
    counter += 1

output.append(arivArea)
transfer = 0
while len(output) > 0 and len(indices) > 0:
    counter = 0
    for route in lines[indices[0]]:
        if route == output[0]:
            strnum = counter
        if route == output[1]:
            arrinum = counter
        counter += 1
    route = lines[indices[0]][output[0]][1]
    if len(indices) > 0:
        indices = indices[1:]
    start = output[0]
    output = output[1:]
    stops = abs(strnum - arrinum)
    if strnum > arrinum:
        route = str.replace(route, 'A', 'R')
    time = stops * 2
    date = 'from_datetime=20191103T12'
    time = date + str(time)
    myUrl = 'https://api.navitia.io/v1/coverage/fr-idf/stop_areas/' + start + '/physical_modes/physical_mode%3AMetro/departures?' + 'from_datetime=20191103T1200'
    if transfer > 0:
        myUrl = 'https://api.navitia.io/v1/coverage/fr-idf/stop_areas/' + start + '/physical_modes/physical_mode%3AMetro/departures?' + time
    head = {'Authorization': myToken}
    response = requests.get(myUrl, headers=head)
    data = response.json()

    for obj in data ['departures']:
        if (obj)['links'][2]['id'] == route:
            depTime = (obj['stop_date_time']['base_departure_date_time'])
            depTime = depTime[9:-4] + ':'+ depTime[11:-2]
            linenum = (obj)['links'][0]['id']
            linenum = linenum[17:]
            print (col.GREEN + '\n' + depTime + '\t Line ' + linenum + '\t\t' + (obj)['route']['direction']['name'] + '\t\t' + "Amount of stops: " + str(stops) + col.RESET)
            break

    if len(indices) > 0:
        for line in lines:
            if output[0] in line.keys():
                print(col.MAGENTA + "\nTransfer on " + (line[output[0]][0]).encode().decode('unicode-escape') + col.RESET)
                break

    transfer += 1
print('\n')