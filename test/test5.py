import json


def getChessList(imageName):
    f = open('D:/xyz/workspace/chessmind/chess/data/json/' + imageName + '.json', encoding='utf-8')
    info = f.read()
    f.close()
    chessDict = json.loads(info)
    chessList = chessDict['results']
    return chessList


def getSortChessList(imageName):
    chesses = getChessList(fileName)
    newChessList = []
    newLocation = {}
    for x in chesses:
        one = x
        newLocation = one['location']
        newLocation['name'] = one['name']
        newLocation['score'] = one['score']
        newChessList.append(newLocation)

    # {'height': 24, 'left': 166, 'top': 107, 'width': 24, 'name': 'kong', 'score': 0.9999850988388062}
    sortChessList = sorted(newChessList, key=lambda w: (w['top'], w['left']), reverse=False)
    # sortChessList = newChessList.sort(key=lambda n: (n['left']))
    # print(sortChessList)
    return sortChessList


fileName = 'chess2'
sortChessesList = getSortChessList(fileName)


# m = 0
# for n in sortChessesList:
#     one = n
#     print(one)
#
#     m = m + 1
#     if m % 5 == 0:
#         print('--------------------------------------')

# x最小值：左上角
minX = min(sortChessesList, key=lambda w: (w['top']))
print(minX)
# x最大值：右上角
maxTop = max(sortChessesList, key=lambda w: (w['top']))
print(maxTop)
# y最小值：左上角
minY = min(sortChessesList, key=lambda w: (w['left']))
print(minY)
# y最大值，右下角
maxY = max(sortChessesList, key=lambda w: (w['left']))
print(maxY)
