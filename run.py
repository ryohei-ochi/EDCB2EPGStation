import csv
import requests
import json

# EPGStationのWebAPI
API_URI = "http://192.168.1.100:8888/api"

# EDCBの自動録画設定ファイル
EDCB_FILE = "C:\EDCB\Setting\EpgAutoAdd.txt"

# チャンネルのSID？変換用辞書
# EDCB:EPGStaion
STATIONS = {
    "0004409000D3": 400211, # BS11
    "00077100014D": 700333 # AT-X
}

# EPGStationの曜日指定用定数
WEEKS = [ 0x01, 0x02, 0x04, 0x08, 0x10, 0x20 ,0x40 ]
WEEK_ALL = 0x7f

# EPGStationのルールIDを全件取得
headers = {
    'accept': 'application/json',
}
response = requests.get(API_URI + '/rules/list', headers=headers)
data = response.json()

# EPGStationのルールを全件削除
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

# EDCBの設定ファイルの読み込み
csv_file = open(EDCB_FILE, "r", encoding="utf-8-sig")

f = csv.reader(csv_file, delimiter="\t", doublequote=False,
    lineterminator="\r\n", quotechar='"', skipinitialspace=True)
for row in f:
    # 行を表示
    print(row)

    # ;;で始まる行は無視
    if not row[0].startswith(";;"):

        # 曜日指定の判定
        # EDCBの期間指定は無視して、期間の始めだけで判定してます
        if row[6] == "":
            week = WEEK_ALL
        else:
            edcb_week = row[6].split(",")
            week = 0
            for tmp in edcb_week:
                week = week | WEEKS[int(tmp[0])]
        
        # EPGStationへ登録するルールを定義
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

        # 除外するキーワードの定義
        if not row[2] == "":
            dic["search"]["ignoreKeyword"] = row[2]
            dic["search"]["ignoreTitle"] = True

        # チャンネル指定の定義
        # TODO:複数のチャンネル指定に対応する
        if row[7] in STATIONS:
            dic["search"]["station"] = STATIONS[row[7]]
            dic["search"]["GR"] = False
            dic["search"]["BS"] = False
            dic["search"]["CS"] = False

        # APIに投げるjsonの表示
        print(json.dumps(dic))

        # EPGStationへルールの追加
        response = requests.post(API_URI + '/rules',
            headers=headers, data=json.dumps(dic))
        
# ルールを予約に反映させる
headers = {
    'accept': 'application/json',
}
response = requests.put(API_URI + '/schedule/update', headers=headers)
data = response.json()

# 結果を表示 200 なら成功
print(data["code"])
