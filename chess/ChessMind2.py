#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json
import numpy as np
import cv2 as cv
from PIL import Image, ImageDraw, ImageFont
from util.ChessTool2 import chess2 as chess

fileName = 'chess2'
toFile = 'D:/xyz/workspace/chessmind/chess/data/images/baidu/' + fileName + 'b.jpg'
# 得到排序的列表
sortChessesList = chess.getSortChessList(fileName)
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
img = chess.drawChess(img, sortChessesList)

cv.imwrite(toFile, img)
cv.namedWindow('chess', cv.WINDOW_NORMAL)
cv.imshow('chess', img)
cv.waitKey()  # 显示 10000 ms 即 10s 后消失
cv.destroyAllWindows()
