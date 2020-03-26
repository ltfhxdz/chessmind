import json

f = open('D:/xyz/workspace/python/ocr/chess/chess2.json', encoding='utf-8')
info = f.read()
f.close()

chessDict = json.loads(info)
chessList = chessDict['results']

for x in chessList:
    one = x
    print(one)
    location = one['location']
    name = one['name']
    score = one['score']
