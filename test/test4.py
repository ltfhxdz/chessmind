# # def takeSecond(elem):
# #     location = elem['location']
# #     print(location)
# #     return location
# #
# from operator import itemgetter
#

# print(chessList)
# # chessList.sort(key=takeSecond)
#
# d = {'data1': 3, 'data2': 1, 'data3': 2, 'data4': 4}
#
# dict1 = {'a': 2, 'e': 3, 'f': 8, 'd': 4}
# dict2 = sorted(dict1)
# print(dict2)


dic = [{"goods_id": 3, "user_id": 11, "score": 0.8},
       {"goods_id": 1, "user_id": 22, "score": 0.1},
       {"goods_id": 2, "user_id": 33, "score": 0.5}]
dic = sorted(dic, key=lambda x: x['score'], reverse=False)
print(dic)

chessList = [{'height': 24, 'left': 167, 'top': 158, 'width': 23},
             {'height': 24, 'left': 166, 'top': 107, 'width': 24},
             {'height': 24, 'left': 191, 'top': 208, 'width': 24}
             ]
chessList = sorted(chessList, key=lambda x: x['left'], reverse=False)
print(chessList)
for i in chessList:
    one = i
    print(one)
    one.update({'name': 'xyz'})
    print(one)

# one = {'height': 24, 'left': 166, 'top': 107, 'width': 24}
# one.update({'name': 'hongshi'})
# print(one)
