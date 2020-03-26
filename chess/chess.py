#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json
import numpy as np
import cv2 as cv
from PIL import Image, ImageDraw, ImageFont


def drawRect(img, left, top, fillColor):
    """打印任何传入的字符串"""
    ptLeftTop = (left, top)  # left,top
    ptRightBottom = (left + 25, top + 25)  # left+width,top+height
    thickness = 1
    lineType = 4
    cv.rectangle(img, ptLeftTop, ptRightBottom, fillColor, thickness, lineType)
    return


def drawFillRect(img, left, top, fillColor):
    """打印任何传入的字符串"""
    ptLeftTop = (left, top)  # left,top
    ptRightBottom = (left + 25, top + 25)  # left+width,top+height
    thickness = -1
    lineType = 4
    cv.rectangle(img, ptLeftTop, ptRightBottom, fillColor, thickness, lineType)
    cv.rectangle(img, ptLeftTop, ptRightBottom, (0, 0, 0), 1, lineType)
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
    img = np.zeros((width, width, 3), np.uint8)  # 生成一个空灰度图像
    img[:, :, 0] = np.zeros([width, width]) + 255
    img[:, :, 1] = np.ones([width, width]) + 254
    img[:, :, 2] = np.ones([width, width]) * 255
    return img


def drawCell(image):
    blue = (255, 0, 0)
    bx = 15
    by = 32
    ex = 215
    ey = 257
    cv.line(image, (bx, by), (ex, by), blue)
    cv.line(image, (bx, by + 25), (ex, by + 25), blue)
    cv.line(image, (bx, by + 25 * 2), (ex, by + 25 * 2), blue)
    cv.line(image, (bx, by + 25 * 3), (ex, by + 25 * 3), blue)
    cv.line(image, (bx, by + 25 * 4), (ex, by + 25 * 4), blue)
    cv.line(image, (bx, by + 25 * 5), (ex, by + 25 * 5), blue)
    cv.line(image, (bx, by + 25 * 6), (ex, by + 25 * 6), blue)
    cv.line(image, (bx, by + 25 * 7), (ex, by + 25 * 7), blue)
    cv.line(image, (bx, by + 25 * 8), (ex, by + 25 * 8), blue)
    cv.line(image, (bx, by + 25 * 9), (ex, by + 25 * 9), blue)

    cv.line(image, (bx, by), (bx, ey), blue)
    cv.line(image, (bx + 25, by), (bx + 25, ey), blue)
    cv.line(image, (bx + 25 * 2, by), (bx + 25 * 2, ey), blue)
    cv.line(image, (bx + 25 * 3, by), (bx + 25 * 3, ey), blue)
    cv.line(image, (bx + 25 * 4, by), (bx + 25 * 4, ey), blue)
    cv.line(image, (bx + 25 * 5, by), (bx + 25 * 5, ey), blue)
    cv.line(image, (bx + 25 * 6, by), (bx + 25 * 6, ey), blue)
    cv.line(image, (bx + 25 * 7, by), (bx + 25 * 7, ey), blue)
    cv.line(image, (bx + 25 * 8, by), (bx + 25 * 8, ey), blue)
    return image


def getChessList(imageName):
    f = open('D:/xyz/workspace/chessmind/chess/data/json/' + imageName + '.json', encoding='utf-8')
    info = f.read()
    f.close()
    chessDict = json.loads(info)
    chessList = chessDict['results']
    return chessList


fileName = 'chess2'
toFile = 'D:/xyz/workspace/chessmind/chess/data/images/baidu/' + fileName + 'b.jpg'

chessMapping = {'hongshuai': '帅', 'hongshi': '士', 'hongxiang': '相', 'hongma': '马', 'hongche': '车',
                'hongpao': '炮', 'hongbing': '兵', 'heijiang': '将', 'heishi': '士', 'heixiang': '象',
                'heima': '马', 'heiche': '车', 'heipao': '炮', 'heizu': '卒', 'kong': '空'}

chesses = getChessList(fileName)
print(chesses)
# print(len(chesses))
# firstChess = chesses[0]
# firstLocation = firstChess['location']
# firstWidth = firstLocation['width']
# firstHeight = firstLocation['height']
# avg = round((firstWidth + firstHeight) / 2)
#

img = drawEmptyRect()
img = drawCell(img)

m = 0
for x in chesses:
    m = m + 1
    one = x
    print(one)
    location = one['location']
    name = one['name']
    score = one['score']
    left = location['left']
    top = location['top']

    if left >= 16:
        continue

    print('xyz:')
    print(one)
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

    # if m == 10:
    #     break

cv.imwrite(toFile, img)

cv.namedWindow("chess", cv.WINDOW_NORMAL)
cv.imshow('chess', img)
cv.waitKey()  # 显示 10000 ms 即 10s 后消失
cv.destroyAllWindows()
