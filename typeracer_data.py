import requests
import json
import time

now = int(time.time())

with open("backup.json", "r") as infile:
    json_object = json.load(infile)

last_time = int(json_object[0]['t'])
data = requests.get(f"https://data.typeracer.com/games?playerId=tr:adi_idgaf&universe=play&startDate={last_time}&endDate={now}")
data_json = data.json()

if len(data_json) == 1:
    print("No races to update!")
else:
    data_json = data_json[:-1]
    data_json.extend(json_object)

    data_json = json.dumps(data_json, indent=4)

    with open("type_data.json", "w") as outfile:
        outfile.write(data_json)

    print("added new races!")
