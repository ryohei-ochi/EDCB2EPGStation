import csv
import requests
import json

API_URI = "http://192.168.1.100:8888/api"
EDCB_FILE = "C:\EDCB\Setting\EpgAutoAdd.txt"
WEEKS = [ 0x01, 0x02, 0x04, 0x08, 0x10, 0x20 ,0x40 ]
WEEK_ALL = 0x7f
# EDCB:EPGStaion
STATIONS = {
    "0004409000D3": 400211, # BS11
    "00077100014D": 700333 # AT-X
}

headers = {
    'accept': 'application/json',
}
response = requests.get(API_URI + '/rules/list', headers=headers)
data = response.json()

id = []
for key in data:
    id.append(key['id'])

dic = {"ruleIds" : id, "delete" : False}
headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
}
response = requests.post(API_URI + '/rules/delete',
    headers=headers, data=json.dumps(dic))

csv_file = open(EDCB_FILE, "r", encoding="utf-8-sig")

f = csv.reader(csv_file, delimiter="\t", doublequote=False,
    lineterminator="\r\n", quotechar='"', skipinitialspace=True)
for row in f:
    print(row)
    if not row[0].startswith(";;"):

        if row[6] == "":
            week = WEEK_ALL
        else:
            edcb_week = row[6].split(",")
            week = 0
            for tmp in edcb_week:
                week = week | WEEKS[int(tmp[0])]
        
        dic = {
            "search": {
                "keyword": row[1],
                "title": True,
                "GR": True,
                "BS": True,
                "CS": True,
                "week": week
            },
            "option": {
                "enable": True,
                "allowEndLack": True
            },
            "encode": {
                "mode1": 0,
                "delTs": False
            }
        }

        if not row[2] == "":
            dic["search"]["ignoreKeyword"] = row[2]
            dic["search"]["ignoreTitle"] = True

        if row[7] in STATIONS:
            dic["search"]["station"] = STATIONS[row[7]]
            dic["search"]["GR"] = False
            dic["search"]["BS"] = False
            dic["search"]["CS"] = False


        print(json.dumps(dic))

        response = requests.post(API_URI + '/rules',
            headers=headers, data=json.dumps(dic))
        
headers = {
    'accept': 'application/json',
}
response = requests.put(API_URI + '/schedule/update', headers=headers)
data = response.json()
print(data["code"])
