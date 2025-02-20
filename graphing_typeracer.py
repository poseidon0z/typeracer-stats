import matplotlib.pyplot as plt
import json

with open("type_data_play.json", "r") as infile:
    json_object = json.load(infile)

json_object.reverse()

json_object = json_object[:]

wpm = [i["wpm"] for i in json_object]
race = [i["gn"] for i in json_object]

smoothness = 10
avg_wpm = []
for i in range(len(wpm) // smoothness):
    a = smoothness * i
    avg_wpm.append(sum(wpm[a : a + smoothness]) / smoothness)

x = len(wpm) % smoothness
if x != 0:
    avg_wpm.append(sum(wpm[-x:]) / x)
race = [i for i in race[::smoothness]]

# print(avg_wpm)
# print(race)

plt.plot(race, avg_wpm)
plt.show()
