#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json
import time
import cv2 as cv
from util.ChessTool2 import chess2 as chess
from util.ChessNetwork import chessnet

start = time.time()

fileName = 'chess2'
imagePath = 'D:/xyz/workspace/chessdata/images/' + fileName + '.jpg'
jsonPath = 'D:/xyz/workspace/chessdata/json/' + fileName + '.json'
chessPath = 'D:/xyz/workspace/chessdata/images/baidu/' + fileName + 'b.jpg'
# 上传文件
chessnet.uploadImage(imagePath, jsonPath)

# 得到排序的列表
sortChessesList = chess.getSortChessList(jsonPath)
print(json.dumps(sortChessesList))
print(len(sortChessesList))

# 显示最大值、最小值
chess.max_min(sortChessesList)

# 初始化画布
img = chess.drawEmptyRect(sortChessesList)

# 棋盘的起始点和最后一块
chess.beginPoint(sortChessesList)
print(json.dumps(sortChessesList))
# 画棋盘
img = chess.drawChessboard(img, sortChessesList)

# 画棋子
# img = chess.drawChess(img, sortChessesList)

# 画逻辑点
logicPointList = chess.drawLogicPoint(sortChessesList, img)
# print(logicPointList)

# 显示棋子
img = chess.showChess(img, logicPointList, sortChessesList)

end = time.time()
print('Running time: %1.2f Seconds' % (end - start))

cv.imwrite(chessPath, img)
cv.namedWindow('chess', cv.WINDOW_NORMAL)
cv.imshow('chess', img)
cv.waitKey()  # 显示 10000 ms 即 10s 后消失
cv.destroyAllWindows()
