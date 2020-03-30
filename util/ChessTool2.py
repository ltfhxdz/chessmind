#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json
import cv2 as cv
import numpy as np
from PIL import Image, ImageDraw, ImageFont


class chess2:

    @staticmethod
    def getChessList(imageName):
        f = open('D:/xyz/workspace/chessmind/chess/data/json/' + imageName + '.json', encoding='utf-8')
        info = f.read()
        f.close()
        chessDict = json.loads(info)
        chessList = chessDict['results']
        return chessList

    @staticmethod
    def drawEmptyRect(sortChessesList):
        qipan = max(sortChessesList, key=lambda w: (w['width']))
        qipanW = qipan['width']
        qipanH = qipan['height']
        # 生成一个空灰度图像
        imageW = qipanW + 300
        imageH = qipanH + 300
        img = np.zeros((imageW, imageH, 3), np.uint8)
        # 白色背景
        img[:, :, 0] = np.zeros([imageW, imageH]) + 255
        img[:, :, 1] = np.ones([imageW, imageH]) + 254
        img[:, :, 2] = np.ones([imageW, imageH]) * 255
        return img

    @staticmethod
    def max_min(sortChessesList):
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
        # qipan
        qipan = max(sortChessesList, key=lambda w: (w['width']))
        print('qipan=' + str(qipan))

    @staticmethod
    def getSortChessList(imageName):
        chesses = chess2.getChessList(imageName)
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

    @staticmethod
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

    @staticmethod
    def drawChess(img, sortChessesList):
        # 画棋子
        m = 0
        for n in sortChessesList:
            m = m + 1
            one = n
            print(one)
            name = one['name']
            score = one['score']
            x = one['x']
            y = one['y']
            width = one['width']
            height = one['height']

            single = ''
            if name != 'kong':
                single = chessMapping[name]

            if 'hong' in name:
                fillColor = (0, 0, 255)
                pt1 = (x, y)
                pt2 = (x + width, y + width)
                cv.rectangle(img, pt1, pt2, fillColor, 1, 4)
                img = chess2.write(img, x, y, single, fillColor)
            elif 'hei' in name:
                fillColor = (0, 0, 0)
                pt1 = (x, y)  # left,top
                pt2 = (x + width, y + width)
                cv.rectangle(img, pt1, pt2, fillColor, 1, 4)
                img = chess2.write(img, x, y, single, fillColor)
            elif 'kong' in name:
                fillColor = (0, 255, 0)
                pt1 = (x, y)  # left,top
                pt2 = (x + width, y + width)
                cv.rectangle(img, pt1, pt2, fillColor, -1, 4)
                # cv.rectangle(img, pt1, pt2, (255, 0, 0), 2, 4)
                img = chess2.write(img, x, y, str(m), (0, 0, 0))
            else:
                print('name=' + name)
        return img

    @staticmethod
    def widthAndHeightAverage(sortChessesList):
        widthAverage = 0
        heightAverage = 0
        for x in sortChessesList:
            one = x
            name = one['name']
            width = one['width']
            height = one['height']
            if 'qipan' in name:
                continue
            widthAverage = widthAverage + width
            heightAverage = heightAverage + height
        widthAverage = widthAverage / (len(sortChessesList) - 1)
        heightAverage = heightAverage / (len(sortChessesList) - 1)
        print('widthAverage = '+str(round(widthAverage)))
        print('heightAverage = '+str(round(heightAverage)))
        averageDict = {'widthAverage': round(widthAverage), 'heightAverage': round(heightAverage)}
        return averageDict

    @staticmethod
    def drawChessboard(img, sortChessesList):
        # 画棋盘

        # 宽的平均值
        averageDict = chess2.widthAndHeightAverage(sortChessesList)
        width = averageDict['widthAverage']
        height = averageDict['heightAverage']

        # 起始点使用棋盘的，宽度使用平均值，宽度使用棋盘，最后画的有些小，百度返回的有些小
        qipan = max(sortChessesList, key=lambda w: (w['width']))
        qipanX = qipan['x']
        qipanY = qipan['y']
        qipanW = width * 8
        qipanH = height * 9

        # pt1 矩形的一个顶点
        pt1 = (qipanX, qipanY)
        # pt2 矩形对角线上的另一个顶点  X+宽 Y+高
        endx = qipanX + qipanW
        endy = qipanY + qipanH
        # print('endx=' + str(endx))
        # print('endy=' + str(endy))
        pt2 = (endx, endy)
        # -1 表示填充，>=1 表示画框线的粗细
        thickness = 1
        cv.rectangle(img, pt1, pt2, (255, 0, 0), thickness, 4)

        # 画横线    X是横坐标 Y是纵坐标
        cv.line(img, (qipanX, qipanY + height * 1), (endx, qipanY + height * 1), (255, 0, 0), thickness)
        cv.line(img, (qipanX, qipanY + height * 2), (endx, qipanY + height * 2), (255, 0, 0), thickness)
        cv.line(img, (qipanX, qipanY + height * 3), (endx, qipanY + height * 3), (255, 0, 0), thickness)
        cv.line(img, (qipanX, qipanY + height * 4), (endx, qipanY + height * 4), (255, 0, 0), thickness)
        cv.line(img, (qipanX, qipanY + height * 5), (endx, qipanY + height * 5), (255, 0, 0), thickness)
        cv.line(img, (qipanX, qipanY + height * 6), (endx, qipanY + height * 6), (255, 0, 0), thickness)
        cv.line(img, (qipanX, qipanY + height * 7), (endx, qipanY + height * 7), (255, 0, 0), thickness)
        cv.line(img, (qipanX, qipanY + height * 8), (endx, qipanY + height * 8), (255, 0, 0), thickness)
        # 最后一行，可能存在误差
        # cv.line(img, (qipanX, qipanY + height * 9), (endx, qipanX + height * 9), (255, 0, 0), 2)
        # 画竖线    X是横坐标 Y是纵坐标
        cv.line(img, (qipanX + width * 1, qipanY), (qipanX + width * 1, endy), (255, 0, 0), thickness)
        cv.line(img, (qipanX + width * 2, qipanY), (qipanX + width * 2, endy), (255, 0, 0), thickness)
        cv.line(img, (qipanX + width * 3, qipanY), (qipanX + width * 3, endy), (255, 0, 0), thickness)
        cv.line(img, (qipanX + width * 4, qipanY), (qipanX + width * 4, endy), (255, 0, 0), thickness)
        cv.line(img, (qipanX + width * 5, qipanY), (qipanX + width * 5, endy), (255, 0, 0), thickness)
        cv.line(img, (qipanX + width * 6, qipanY), (qipanX + width * 6, endy), (255, 0, 0), thickness)
        cv.line(img, (qipanX + width * 7, qipanY), (qipanX + width * 7, endy), (255, 0, 0), thickness)
        # 最后一列，可能存在误差 误差是 endx- (qipanX + width * 8)=6
        # cv.line(img, (qipanX + width * 8, qipanY), (qipanX + width * 8, endy), (255, 0, 0), 2)
        # print(qipanX + width * 8)
        return img


chessMapping = {'hongshuai': '帅', 'hongshi': '士', 'hongxiang': '相', 'hongma': '马', 'hongche': '车',
                'hongpao': '炮', 'hongbing': '兵', 'heijiang': '将', 'heishi': '士', 'heixiang': '象',
                'heima': '马', 'heiche': '车', 'heipao': '炮', 'heizu': '卒', 'kong': '空',
                'qipan': 'qipan', 'chuhe': 'chuhe'}
