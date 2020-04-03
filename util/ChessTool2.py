#!/usr/bin/python
# -*- coding: UTF-8 -*-
import math
import json
import cv2 as cv
import numpy as np
from PIL import Image, ImageDraw, ImageFont


class chess2:

    @staticmethod
    def getChessList(filePath):
        f = open(filePath, encoding='utf-8')
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
        # 棋子的宽和高使用平均值，目的是为了棋子的一致性
        widthAverage = averageDict['widthAverage']
        heightAverage = averageDict['heightAverage']

        for n in sortChessesList:
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

            place = one.get('place')
            print(place)

            single = ''
            if name != 'kong':
                single = chessMapping[name]

            if 'hong' in name:
                # 起始点或终点就画蓝色
                if place is None:
                    color = (0, 0, 255)
                else:
                    color = (255, 0, 0)

                pt1 = (x, y)
                pt2 = (x + width, y + height)
                cv.rectangle(img, pt1, pt2, color, -1, 4)
                # 不能复用颜色 opencv和PIL颜色规则不一样
                img = chess2.write(img, x, y, single, (255, 255, 255))
            elif 'hei' in name:
                # 起始点或终点就画蓝色
                if place is None:
                    color = (0, 0, 0)
                else:
                    color = (255, 0, 0)
                pt1 = (x, y)  # left,top
                pt2 = (x + width, y + height)
                cv.rectangle(img, pt1, pt2, color, -1, 4)
                img = chess2.write(img, x, y, single, (255, 255, 255))
            elif 'kong' in name:
                # 起始点或终点就画蓝色
                if place is None:
                    color = (0, 255, 0)
                else:
                    color = (255, 0, 0)
                pt1 = (x, y)  # left,top
                pt2 = (x + width, y + height)
                # cv.rectangle(img, pt1, pt2, color, -1, 4)
                # # img = chess2.write(img, x, y, str(m), (0, 0, 0))
                # img = chess2.write(img, x, y, '', (0, 0, 0))
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
        # 位置信息
        beginx, beginy, endx, endy, width, height = chess2.placeInfo(sortChessesList)

        # pt1 矩形的一个顶点
        pt1 = (beginx, beginy)
        # pt2 矩形对角线上的另一个顶点  X+宽 Y+高
        pt2 = (endx, endy)
        # -1 表示填充，>=1 表示画框线的粗细
        thickness = 2
        color = (0, 0, 0)
        cv.rectangle(img, pt1, pt2, color, thickness, 4)

        # 画横线    X是横坐标 Y是纵坐标
        for a in range(1, 9):
            cv.line(img, (beginx, beginy + height * a), (endx, beginy + height * a), color, thickness)

        # 画竖线    X是横坐标 Y是纵坐标
        for a in range(1, 8):
            cv.line(img, (beginx + width * a, beginy), (beginx + width * a, endy), color, thickness)

        return img

    @staticmethod
    def placeInfo(sortChessesList):
        # 起始点
        beginPoint = min(sortChessesList, key=lambda w: (w['begin']))
        beginPoint['place'] = 'start'
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
        endPoint['place'] = 'finish'
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
        return beginx, beginy, endx, endy, width, height

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

    @staticmethod
    def drawLogicPoint(sortChessesList, img):
        """画逻辑点"""
        # 位置信息
        beginx, beginy, endx, endy, width, height = chess2.placeInfo(sortChessesList)

        A = int(beginx - width / 4)
        B = int(beginy - height / 4)
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
                fillColor = (0, 255, 0)
                # cv.rectangle(img, pt1, pt2, fillColor, -1, 4)
        return logicPointList

    @staticmethod
    def drawLogicPoint2(sortChessesList, img):
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
                fillColor = (0, 255, 0)
                cv.rectangle(img, pt1, pt2, fillColor, -1, 4)
        return logicPointList

    @staticmethod
    def showChess(img, logicPointList, sortChessesList):
        # 如果逻辑点被包围，就显示棋子
        for i in logicPointList:
            logicPointBox = {}
            logicPointBox.update({'x': i['x'], 'y': i['y'], 'width': i['width'], 'height': i['height']})

            for n in sortChessesList:
                one = n
                name = one['name']
                x = one['x']
                y = one['y']
                width = one['width']
                height = one['height']
                sortChessBox = {}
                sortChessBox.update({'x': x, 'y': y, 'width': width, 'height': height})

                if 'qipan' == name:
                    continue

                if chess2.chonghe(sortChessBox, logicPointBox):
                    single = ''
                    if name != 'kong':
                        single = chessMapping[name]

                    if 'hong' in name:
                        color = (0, 0, 255)
                        pt1 = (x, y)
                        pt2 = (x + width, y + height)
                        cv.rectangle(img, pt1, pt2, color, -1, 4)
                        # 不能复用颜色 opencv和PIL颜色规则不一样
                        img = chess2.write(img, x, y, single, (255, 255, 255))
                    elif 'hei' in name:
                        color = (0, 0, 0)
                        pt1 = (x, y)  # left,top
                        pt2 = (x + width, y + height)
                        cv.rectangle(img, pt1, pt2, color, -1, 4)
                        img = chess2.write(img, x, y, single, (255, 255, 255))
                    else:
                        print('name=' + name)
                    break
        return img

    @staticmethod
    def chonghe(box1, bofinal):
        """bofinal落在了box1里"""
        x01 = box1['x']
        y01 = box1['y']
        box1w = box1['width']
        box1h = box1['height']
        x11 = bofinal['x']
        y11 = bofinal['y']
        bofinalw = bofinal['width']
        bofinalh = bofinal['height']

        x02 = x01 + box1w
        y02 = y01 + box1h
        x12 = x11 + bofinalw
        y12 = y11 + bofinalh

        if (x01 <= x11) and (y01 <= y12) and (x02 >= x12) and (y02 >= y12):
            return True
        else:
            return False

    @staticmethod
    def drawBlackChess(img, word, left, top):
        fillColor = (0, 0, 0)
        chess2.drawRect(img, left, top, fillColor)
        img = chess2.write(img, left, top, word, fillColor)
        return img

    @staticmethod
    def drawRedChess(img, word, left, top):
        chess2.drawRect(img, left, top, (0, 0, 255))
        img = chess2.write(img, left, top, word, (255, 0, 0))
        return img

    @staticmethod
    def drawKongChess(img, word, left, top):
        chess2.drawFillRect(img, left, top, (0, 255, 0))
        img = chess2.write(img, left, top, word, (0, 255, 0))
        return img

    @staticmethod
    def drawRect(img, left, top, fillColor):
        """画方框"""
        pt1 = (left, top)  # left,top
        pt2 = (left + 25, top + 25)  # left+width,top+height
        thickness = 1
        lineType = 4
        cv.rectangle(img, pt1, pt2, fillColor, thickness, lineType)
        return


chessMapping = {'hongshuai': '帅', 'hongshi': '士', 'hongxiang': '相', 'hongma': '马', 'hongche': '车',
                'hongpao': '炮', 'hongbing': '兵', 'heijiang': '将', 'heishi': '士', 'heixiang': '象',
                'heima': '马', 'heiche': '车', 'heipao': '炮', 'heizu': '卒', 'kong': '空',
                'qipan': 'qipan', 'chuhe': 'chuhe'}
