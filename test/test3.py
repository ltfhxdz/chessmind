#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json


def getChessList(imageName):
    f = open('D:/xyz/workspace/chessmind/chess/data/json/' + imageName + '.json', encoding='utf-8')
    info = f.read()
    f.close()
    chessDict = json.loads(info)
    chessList = chessDict['results']
    return chessList


fileName = 'chess2'
chessMapping = {'hongshuai': '帅', 'hongshi': '士', 'hongxiang': '相', 'hongma': '马', 'hongche': '车',
                'hongpao': '炮', 'hongbing': '兵', 'heijiang': '将', 'heishi': '士', 'heixiang': '象',
                'heima': '马', 'heiche': '车', 'heipao': '炮', 'heizu': '卒'}

chesses = getChessList(fileName)
for x in chesses:
    one = x
    print(one)
    location = one['location']
    name = one['name']
    score = one['score']
    left = location['left']
    top = location['top']

    if name != 'kong':
        chess = chessMapping[name]

    if 'hong' in name:
        pass
    elif 'hei' in name:
        pass
    else:
        print('name=' + name)
