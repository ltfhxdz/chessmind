#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json
import numpy as np
import cv2 as cv
from PIL import Image, ImageDraw, ImageFont
from util.ChessTool import chess


fileName = 'chess2'
toFile = 'D:/xyz/workspace/chessmind/chess/data/images/baidu/' + fileName + 'b.jpg'

sortChessesList = chess.getSortChessList(fileName)
print(sortChessesList)
chess.max_min(sortChessesList)

minX = min(sortChessesList, key=lambda w: (w['x']))
print('minX=' + str(minX))
img = chess.drawEmptyRect()
chess.drawCell(img, minX)
logicPointList = chess.drawLogicPoint(sortChessesList, img)
# 显示棋子
img = chess.showChess(img, logicPointList, sortChessesList)

cv.imwrite(toFile, img)
cv.namedWindow("chess", cv.WINDOW_NORMAL)
cv.imshow('chess', img)
cv.waitKey()  # 显示 10000 ms 即 10s 后消失
cv.destroyAllWindows()

