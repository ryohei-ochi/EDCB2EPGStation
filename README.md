## 何ができるの
xtne6f版EDCBの自動録画設定を、EPGStaionのルールに反映させることができます。

## 開発環境

- Python 3.8 (Windows10 x64) 
- VSCode（Visual Studio Code） 

## 動作環境

PythonからEPGStatinのWebAPIを叩いて動作しています。  
requestsモジュールが必要だと思います。  

`pip install requests`

## 使用方法
**1、環境設定**  
`API_URI`と`EDCB_FILE`を環境に合わせて変更してください。  
いまのところチャンネル指定は、BS11とAT-Xしか対応していません。  
複数のチャンネル指定があった場合も判定をサボっているので、GR、BS、CSがルールの検索対象になります。  

`STATIONS`で定義できますので、地上波は難しいですが、BSとCSをどなたか完成させてください(笑)

**2、実行**  
`python run.py`
  
正常系しか実装していないので、実行結果をEPGStaionのルール画面と、予約画面で確認してください。

---
## 注意事項
すでに登録されているEPGStaionのルールは、全て削除されます。