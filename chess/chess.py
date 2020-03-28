#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time
import json
import numpy as np
import cv2 as cv
from PIL import Image, ImageDraw, ImageFont


def drawRect(img, left, top, fillColor):
    """画方框"""
    pt1 = (left, top)  # left,top
    pt2 = (left + 25, top + 25)  # left+width,top+height
    thickness = 1
    lineType = 4
    cv.rectangle(img, pt1, pt2, fillColor, thickness, lineType)
    return


def drawFillRect(img, left, top, fillColor):
    """画方"""
    # pt1 矩形的一个顶点
    # pt2 矩形对角线上的另一个顶点
    pt1 = (left, top)  # left,top
    pt2 = (left + 25, top + 25)  # left+width,top+height
    # -1 表示填充，1 表示画框
    thickness = -1
    lineType = 4
    cv.rectangle(img, pt1, pt2, fillColor, thickness, lineType)
    cv.rectangle(img, pt1, pt2, (255, 0, 0), 1, lineType)
    return


def write(img, left, top, word, fillColor):
    # 将opencv图像格式转换成PIL格式
    img_PIL = Image.fromarray(cv.cvtColor(img, cv.COLOR_BGR2RGB))

    font = ImageFont.truetype('simhei.ttf', 26)
    position = (left, top)  # 文字输出位置
    draw = ImageDraw.Draw(img_PIL)
    draw.text(position, word, font=font, fill=fillColor)

    # 将PIL图像格式转换成opencv格式
    img = cv.cvtColor(np.asarray(img_PIL), cv.COLOR_RGB2BGR)
    return img


def drawBlackChess(img, word, left, top):
    fillColor = (0, 0, 0)
    drawRect(img, left, top, fillColor)
    img = write(img, left, top, word, fillColor)
    return img


def drawRedChess(img, word, left, top):
    drawRect(img, left, top, (0, 0, 255))
    img = write(img, left, top, word, (255, 0, 0))
    return img


def drawKongChess(img, word, left, top):
    drawFillRect(img, left, top, (0, 255, 0))
    img = write(img, left, top, word, (0, 255, 0))
    return img


def drawEmptyRect():
    width = 600
    # 生成一个空灰度图像
    img = np.zeros((width, width, 3), np.uint8)
    # 白色背景
    img[:, :, 0] = np.zeros([width, width]) + 255
    img[:, :, 1] = np.ones([width, width]) + 254
    img[:, :, 2] = np.ones([width, width]) * 255
    return img


def drawCell(image, minX):
    blue = (255, 0, 0)
    bx = minX['x']
    by = minX['y']
    width = minX['width']
    ex = 215
    ey = 257
    cv.line(image, (bx, by), (ex, by), blue)
    cv.line(image, (bx, by + width), (ex, by + width), blue)
    cv.line(image, (bx, by + width * 2), (ex, by + width * 2), blue)
    cv.line(image, (bx, by + width * 3), (ex, by + width * 3), blue)
    cv.line(image, (bx, by + width * 4), (ex, by + width * 4), blue)
    cv.line(image, (bx, by + width * 5), (ex, by + width * 5), blue)
    cv.line(image, (bx, by + width * 6), (ex, by + width * 6), blue)
    cv.line(image, (bx, by + width * 7), (ex, by + width * 7), blue)
    cv.line(image, (bx, by + width * 8), (ex, by + width * 8), blue)
    cv.line(image, (bx, by + width * 9), (ex, by + width * 9), blue)

    cv.line(image, (bx, by), (bx, ey), blue)
    cv.line(image, (bx + width, by), (bx + width, ey), blue)
    cv.line(image, (bx + width * 2, by), (bx + width * 2, ey), blue)
    cv.line(image, (bx + width * 3, by), (bx + width * 3, ey), blue)
    cv.line(image, (bx + width * 4, by), (bx + width * 4, ey), blue)
    cv.line(image, (bx + width * 5, by), (bx + width * 5, ey), blue)
    cv.line(image, (bx + width * 6, by), (bx + width * 6, ey), blue)
    cv.line(image, (bx + width * 7, by), (bx + width * 7, ey), blue)
    cv.line(image, (bx + width * 8, by), (bx + width * 8, ey), blue)
    return image


def chonghe(box1, box2):
    """box2落在了box1里"""
    x01 = box1['x']
    y01 = box1['y']
    box1w = box1['width']
    box1h = box1['height']
    x11 = box2['x']
    y11 = box2['y']
    box2w = box2['width']
    box2h = box2['height']

    x02 = x01 + box1w
    y02 = y01 + box1h
    x12 = x11 + box2w
    y12 = y11 + box2h

    if (x01 <= x11) and (y01 <= y12) and (x02 >= x12) and (y02 >= y12):
        return True
    else:
        return False


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
    for x in chesses:
        newOne = x
        newLocation = {'name': newOne['name'],
                       'x': newOne['location']['left'],
                       'y': newOne['location']['top'],
                       'width': newOne['location']['width'],
                       'height': newOne['location']['height'],
                       'score': newOne['score']}
        newChessList.append(newLocation)

    sortChessList = sorted(newChessList, key=lambda w: (w['y'], w['x']), reverse=False)
    return sortChessList


def max_min():
    # x最小值：左上角
    minX = min(sortChessesList, key=lambda w: (w['x']))
    print('minX=' + str(minX))
    # x最大值：右上角
    maxX = max(sortChessesList, key=lambda w: (w['x']))
    print('maxX=' + str(maxX))
    # y最小值：左上角
    minY = min(sortChessesList, key=lambda w: (w['y']))
    print('minY=' + str(minY))
    # y最大值，右下角
    maxY = max(sortChessesList, key=lambda w: (w['y']))
    print('maxY=' + str(maxY))


def drawLogicPoint(sortChessesList):
    """画逻辑点"""
    minX = min(sortChessesList, key=lambda w: (w['x']))

    D11x = minX['x']
    D11y = minX['y']
    width = minX['width']
    height = minX['height']
    A = int(D11x - width / 4)
    B = int(D11y - height / 4)
    W = int(width / 2)
    H = int(height / 2)

    logicPointList = []
    for a in range(0, 10):
        B1 = B + height * a
        for b in range(0, 9):
            A1 = A + width * b
            pt1 = (A1, B1)
            pt2 = (A1 + W, B1 + H)
            logicPointName = 'D' + str(a + 1) + str(b + 1)
            logicPointDict = {}
            logicPointDict.update({'name': logicPointName, 'x': A1, 'y': B1, 'width': W, 'height': H})
            logicPointList.append(logicPointDict)
            fillColor = (0, 0, 0)
            cv.rectangle(img, pt1, pt2, fillColor, -1, 4)
    return logicPointList


def showChess(img, logicPointList, sortChessesList):
    # 如果逻辑点被包围，就显示棋子
    for i in logicPointList:
        logicPointBox = {}
        logicPointBox.update({'x': i['x'], 'y': i['y'], 'width': i['width'], 'height': i['height']})

        for n in sortChessesList:
            one = n
            name = one['name']
            score = one['score']
            left = one['x']
            top = one['y']
            width = one['width']
            height = one['height']
            sortChessBox = {}
            sortChessBox.update({'x': left, 'y': top, 'width': width, 'height': height})

            if chonghe(sortChessBox, logicPointBox):
                chess = ''
                if name != 'kong':
                    chess = chessMapping[name]

                if 'hong' in name:
                    img = drawRedChess(img, chess, left, top)
                elif 'hei' in name:
                    img = drawBlackChess(img, chess, left, top)
                elif 'kong' in name:
                    img = drawKongChess(img, chess, left, top)
                else:
                    print('name=' + name)
                break
    return img


fileName = 'chess2'
toFile = 'D:/xyz/workspace/chessmind/chess/data/images/baidu/' + fileName + 'b.jpg'

chessMapping = {'hongshuai': '帅', 'hongshi': '士', 'hongxiang': '相', 'hongma': '马', 'hongche': '车',
                'hongpao': '炮', 'hongbing': '兵', 'heijiang': '将', 'heishi': '士', 'heixiang': '象',
                'heima': '马', 'heiche': '车', 'heipao': '炮', 'heizu': '卒', 'kong': '空'}

sortChessesList = getSortChessList(fileName)
print(sortChessesList)
max_min()

minX = min(sortChessesList, key=lambda w: (w['x']))
print('minX=' + str(minX))
img = drawEmptyRect()
drawCell(img, minX)
logicPointList = drawLogicPoint(sortChessesList)
# 显示棋子
img = showChess(img, logicPointList, sortChessesList)

cv.imwrite(toFile, img)
cv.namedWindow("chess", cv.WINDOW_NORMAL)
cv.imshow('chess', img)
cv.waitKey()  # 显示 10000 ms 即 10s 后消失
cv.destroyAllWindows()
