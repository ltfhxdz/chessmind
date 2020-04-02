#!/usr/bin/python
# -*- coding: UTF-8 -*-
import math
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
        # TODO 分辨率还存在调整 300 600
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
        averageDict = chess2.widthAndHeightAverage(sortChessesList)
        widthAverage = averageDict['widthAverage']
        heightAverage = averageDict['heightAverage']

        m = 0
        for n in sortChessesList:
            m = m + 1
            one = n
            # print(one)
            name = one['name']
            score = one['score']
            x = one['x']
            y = one['y']
            # 使用平均值的宽和高
            # width = one['width']
            # height = one['height']
            width = widthAverage
            height = heightAverage

            location = one.get('location')

            single = ''
            if name != 'kong':
                single = chessMapping[name]

            if 'hong' in name:
                if location is None:
                    color = (0, 0, 255)
                else:
                    color = (255, 0, 0)

                pt1 = (x, y)
                pt2 = (x + width, y + height)
                cv.rectangle(img, pt1, pt2, color, -1, 4)
                # 不能复用颜色 opencv和PIL颜色规则不一样
                img = chess2.write(img, x, y, single, (255, 255, 255))
            elif 'hei' in name:
                if location is None:
                    color = (0, 0, 0)
                else:
                    color = (255, 0, 0)
                pt1 = (x, y)  # left,top
                pt2 = (x + width, y + height)
                cv.rectangle(img, pt1, pt2, color, -1, 4)
                img = chess2.write(img, x, y, single, (255, 255, 255))
            elif 'kong' in name:
                if location is None:
                    color = (0, 255, 0)
                else:
                    color = (255, 0, 0)
                pt1 = (x, y)  # left,top
                pt2 = (x + width, y + height)
                cv.rectangle(img, pt1, pt2, color, -1, 4)
                # img = chess2.write(img, x, y, str(m), (0, 0, 0))
                img = chess2.write(img, x, y, '', (0, 0, 0))
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
        print('widthAverage = ' + str(round(widthAverage)))
        print('heightAverage = ' + str(round(heightAverage)))
        averageDict = {'widthAverage': round(widthAverage), 'heightAverage': round(heightAverage)}
        return averageDict

    @staticmethod
    def drawChessboard(img, sortChessesList):
        # 画棋盘
        chess2.drawQipan(img, sortChessesList)

        # 起始点
        beginPoint = min(sortChessesList, key=lambda w: (w['begin']))
        beginPoint['location'] = 'start'
        print('beginPoint=' + str(beginPoint))

        beginx = beginPoint['x']
        beginy = beginPoint['y']
        beginw = beginPoint['width']
        beginh = beginPoint['height']

        name = beginPoint['name']
        if 'kong' not in name:
            point = beginPoint.get('point')
            if point == 1:
                # 1中心点：x+width/2,y+height/2
                # 1起始点：1的中心点
                beginx = beginx + round(beginw / 2)
                beginy = beginy + round(beginh / 2)
            elif point == 2:
                print(point)
                # 2中心点：x+width/2,y+height/2
                # 2起始点：2的中心点x,y-height
                beginx = beginx + round(beginw / 2)
                beginy = beginy + round(beginh / 2) - beginh
            elif point == 3:
                print(point)
                # 3起始点：3的中心点x-width,y
                # 3中心点：x+width/2,y+height/2
                beginx = (beginx - beginw) + round(beginw / 2)
                beginy = beginy + round(beginh / 2)
            elif point == 4:
                print(point)
                # 4中心点：x+width/2,y+height/2
                # 4起始点：4的中心点x-width,y-height
                beginx = (beginx + round(beginw / 2)) - beginw
                beginy = (beginy + round(beginh / 2)) - beginh

        # 终点
        endPoint = min(sortChessesList, key=lambda w: (w['end']))
        endPoint['location'] = 'finish'
        print('endPoint=' + str(endPoint))
        endPointX = endPoint['x']
        endPointY = endPoint['y']
        endPointW = endPoint['width']
        endPointH = endPoint['height']

        endx = endPointX + endPointW
        endy = endPointY + endPointH

        name = endPoint['name']
        if 'kong' not in name:
            point = endPoint.get('point')
            if point == 5:
                # 5中心点：x+width/2,y+height/2
                # 5终点：5的中心点
                endx = endPointX + round(endPointW / 2)
                endy = endPointY + round(endPointH / 2)
            elif point == 6:
                print(point)
                # 6中心点：x+width/2,y+height/2
                # 6终点：6的中心点x,y+height
                endx = endPointX + round(endPointW / 2)
                endy = endPointY + round(endPointH / 2) + endPointH
            elif point == 7:
                print(point)
                # 7中心点：x+width/2,y+height/2
                # 7终点：7的中心点x+width,y
                endx = endPointX + round(endPointW / 2) + endPointW
                endy = endPointY + round(endPointH / 2)
            elif point == 8:
                print(point)
                # 8中心点：x+width/2,y+height/2
                # 8终点：8的中心点x+width,y+height
                endx = endPointX + round(endPointW / 2) + endPointW
                endy = endPointY + round(endPointH / 2) + endPointH

        width = round((endx - beginx) / 8)
        height = round((endy - beginy) / 9)

        # pt1 矩形的一个顶点
        pt1 = (beginx, beginy)
        # pt2 矩形对角线上的另一个顶点  X+宽 Y+高
        pt2 = (endx, endy)
        # -1 表示填充，>=1 表示画框线的粗细
        thickness = 1
        color = (0, 0, 0)
        cv.rectangle(img, pt1, pt2, color, thickness, 4)

        # 画横线    X是横坐标 Y是纵坐标
        cv.line(img, (beginx, beginy + height * 1), (endx, beginy + height * 1), color, thickness)
        cv.line(img, (beginx, beginy + height * 2), (endx, beginy + height * 2), color, thickness)
        cv.line(img, (beginx, beginy + height * 3), (endx, beginy + height * 3), color, thickness)
        cv.line(img, (beginx, beginy + height * 4), (endx, beginy + height * 4), color, thickness)
        cv.line(img, (beginx, beginy + height * 5), (endx, beginy + height * 5), color, thickness)
        cv.line(img, (beginx, beginy + height * 6), (endx, beginy + height * 6), color, thickness)
        cv.line(img, (beginx, beginy + height * 7), (endx, beginy + height * 7), color, thickness)
        cv.line(img, (beginx, beginy + height * 8), (endx, beginy + height * 8), color, thickness)

        # 画竖线    X是横坐标 Y是纵坐标
        cv.line(img, (beginx + width * 1, beginy), (beginx + width * 1, endy), color, thickness)
        cv.line(img, (beginx + width * 2, beginy), (beginx + width * 2, endy), color, thickness)
        cv.line(img, (beginx + width * 3, beginy), (beginx + width * 3, endy), color, thickness)
        cv.line(img, (beginx + width * 4, beginy), (beginx + width * 4, endy), color, thickness)
        cv.line(img, (beginx + width * 5, beginy), (beginx + width * 5, endy), color, thickness)
        cv.line(img, (beginx + width * 6, beginy), (beginx + width * 6, endy), color, thickness)
        cv.line(img, (beginx + width * 7, beginy), (beginx + width * 7, endy), color, thickness)

        return img

    @staticmethod
    def drawQipan(img, sortChessesList):
        qipan = max(sortChessesList, key=lambda w: (w['width']))
        qipanX = qipan['x']
        qipanY = qipan['y']
        qipanW = qipan['width']
        qipanH = qipan['height']
        qipanBegin = (qipanX, qipanY)
        qianEnd = (qipanX + qipanW, qipanY + qipanH)
        # -1 表示填充，>=1 表示画框线的粗细
        thickness = 1
        color = (255, 0, 0)
        cv.rectangle(img, qipanBegin, qianEnd, color, thickness, 4)

    @staticmethod
    def beginPoint(sortChessesList):
        qipan = max(sortChessesList, key=lambda ww: (ww['width']))
        qipanX = qipan['x']
        qipanY = qipan['y']
        qipanW = qipan['width']
        qipanH = qipan['height']
        endX = qipanX + qipanW
        endY = qipanY + qipanH

        for n in sortChessesList:
            one = n
            # print(one)
            name = one['name']

            if 'qipan' in name:
                n['begin'] = 10000
                n['end'] = 10000
                continue

            x = one['x']
            y = one['y']
            w = one['width']
            h = one['height']
            ex = x + w
            ey = y + h

            begin = round(math.sqrt(math.pow(abs(qipanX - x), 2) + math.pow(abs(qipanY - y), 2)))
            n['begin'] = begin
            # 在分析是否1点、2点、3点、4点
            # 1点  1x<=Qx,1y<=Qy,Qx-1x<=width,Qy-1y<=height
            if x <= qipanX and y <= qipanY and abs(qipanX - x) <= w and abs(qipanY - y) <= h:
                n['point'] = 1
            # 2点  2x<=Qx,2y>=Qy ,Qx-2x<=width,Qy-2y<=height
            if x <= qipanX and y >= qipanY and abs(qipanX - x) <= w and abs(qipanY - y) <= h:
                n['point'] = 2
            # 3点  3x>=Qx,3y<=Qy ,Qx-3x<=width,Qy-3y<=height
            if x >= qipanX and y <= qipanY and abs(qipanX - x) <= w and abs(qipanY - y) <= h:
                n['point'] = 3
            # 4点  4x>=Qx,4y>=Qy ,Qx-4x<=width,Qy-4y<=height
            if x >= qipanX and y >= qipanY and abs(qipanX - x) <= w and abs(qipanY - y) <= h:
                n['point'] = 4

            end = round(math.sqrt(math.pow(abs(endX - ex), 2) + math.pow(abs(endY - ey), 2)))
            n['end'] = end
            # 在分析是否5点、6点、7点、8点
            # 5点  qx-5x<width 	qy-5y<height
            if (abs(endX - x) < w) and (abs(endY - y) < h):
                n['point'] = 5
                print(n)
            # 6点 6点  qx-6x<width  	qy-6y<height*2
            if (abs(endX - x) < w) and (abs(endY - y) < h * 2) and (abs(endY - y) > h):
                n['point'] = 6
                print(n)
            # 7点  qx-7x<width*2  	qy-7y<height
            if (abs(endX - x) < w * 2) and (abs(endX - x) > w) and (abs(endY - y) < h):
                n['point'] = 7
                print(n)
            # 8点  qx-8x<width*2	qy-8y<height*2
            if (abs(endX - x) < w * 2) and (abs(endY - y) < h * 2) and (abs(endX - x) >= w) and (abs(endY - y) > h):
                n['point'] = 8
                print(n)

        # 继续寻找是否比起始点更前的棋子：X<Bx,Y<=By+Bw/2
        beginPoint = min(sortChessesList, key=lambda a: (a['begin']))
        beginX = beginPoint['x']
        beginY = beginPoint['y']
        beginW = beginPoint['width']
        for n in sortChessesList:
            one = n
            x = one['x']
            y = one['y']
            w = one['width']
            name = one['name']
            if 'qipan' in name:
                continue

            if x < beginX and y <= (beginY + round(beginW / 2)):
                one['begin'] = 0


chessMapping = {'hongshuai': '帅', 'hongshi': '士', 'hongxiang': '相', 'hongma': '马', 'hongche': '车',
                'hongpao': '炮', 'hongbing': '兵', 'heijiang': '将', 'heishi': '士', 'heixiang': '象',
                'heima': '马', 'heiche': '车', 'heipao': '炮', 'heizu': '卒', 'kong': '空',
                'qipan': 'qipan', 'chuhe': 'chuhe'}
