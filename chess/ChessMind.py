#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json
import numpy as np
import cv2 as cv
from PIL import Image, ImageDraw, ImageFont
from util.ChessTool import chess


fileName = 'chess2'
toFile = 'D:/xyz/workspace/chessmind/chess/data/images/baidu/' + fileName + 'b.jpg'
# 得到排序的列表
sortChessesList = chess.getSortChessList(fileName)
print(json.dumps(sortChessesList))
print(len(sortChessesList))
# 显示最大值、最小值
chess.max_min(sortChessesList)

# 画空格子
width = 600
img = chess.drawEmptyRect(width)

# 画棋盘
# img = chess.drawChessboard(sortChessesList)
#
# # 画棋子
chess.drawChess(img, sortChessesList)
# minX={'name': 'kong', 'x': 23, 'y': 858, 'width': 109, 'height': 100, 'score': 0.9999998807907104}
# pt1 矩形的一个顶点
# pt1 = (23, 858)
# # pt2 矩形对角线上的另一个顶点  X+宽 Y+高
# pt2 = (23 + 109, 858 + 100)
# # -1 表示填充，1 表示画框, >=2表示线的粗细
# cv.rectangle(img, pt1, pt2, (255, 0, 0), 2, 4)


# # 画格子
chess.drawCell(img, sortChessesList)
# # 画逻辑点
# logicPointList = chess.drawLogicPoint(sortChessesList, img)
# # 显示棋子
# img = chess.showChess(img, logicPointList, sortChessesList)

cv.imwrite(toFile, img)
cv.namedWindow("chess", cv.WINDOW_NORMAL)
cv.imshow('chess', img)
cv.waitKey()  # 显示 10000 ms 即 10s 后消失
cv.destroyAllWindows()

