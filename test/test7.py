import cv2 as cv
import numpy as np


def intersect(box1, bofinal):
    # 判断两个矩形是否相交
    # box=(xA,yA,xB,yB)
    x01, y01, x02, y02 = box1
    x11, y11, x12, y12 = bofinal

    lx = abs((x01 + x02) / 2 - (x11 + x12) / 2)
    ly = abs((y01 + y02) / 2 - (y11 + y12) / 2)
    sax = abs(x01 - x02)
    sbx = abs(x11 - x12)
    say = abs(y01 - y02)
    sby = abs(y11 - y12)
    if lx <= (sax + sbx) / 2 and ly <= (say + sby) / 2:
        return True
    else:
        return False


def chonghe6(box1, bofinal):
    # box=(xA,yA,xB,yB)
    # 计算两个矩形框的重合度
    print(box1)
    print(bofinal)
    if intersect(box1, bofinal):
        x01, y01, x02, y02 = box1
        x11, y11, x12, y12 = bofinal
        col = min(x02, x12) - max(x01, x11)
        print('col=' + str(col))
        row = min(y02, y12) - max(y01, y11)
        print('row=' + str(row))
        intersection = col * row
        print('intersection=' + str(intersection))
        area1 = (x02 - x01) * (y02 - y01)
        print('area1=' + str(area1))
        area2 = (x12 - x11) * (y12 - y11)
        print('area2=' + str(area2))
        coincide = intersection / (area1 + area2 - intersection)
        print('coincide=' + str(coincide))
        return coincide
    else:
        return False


def chonghe2(box1, bofinal):
    x01, y01, x02, y02 = box1
    x11, y11, x12, y12 = bofinal

    if x01 > x11 + x12:
        return 0.0
    if y01 > y11 + y12:
        return 0.0
    if x01 + x02 < x11:
        return 0.0
    if y01 + y02 < y11:
        return 0.0
    colInt = min(x01 + x02, x11 + x12) - max(x01, x11)
    rowInt = min(y01 + y02, y11 + y12) - max(y01, y11)
    intersection = colInt * rowInt
    area1 = x02 * y02
    area2 = x12 * y12
    coincide2 = intersection / (area1 + area2 - intersection)
    print('colInt=' + str(colInt))
    print('rowInt=' + str(rowInt))
    print('intersection=' + str(intersection))
    print('area1=' + str(area1))
    print('area2=' + str(area2))
    print('coincide2=' + str(coincide2))
    return coincide2


def drawFillRect(image, left, top, w, h, color):
    """画方"""
    # pt1 矩形的一个顶点
    # pt2 矩形对角线上的另一个顶点
    pt1 = (left, top)  # left,top
    pt2 = (left + w, top + h)  # left+width,top+height
    # -1 表示填充，1 表示画框
    thickness = -1
    lineType = 4
    cv.rectangle(image, pt1, pt2, color, thickness, lineType)
    cv.rectangle(image, pt1, pt2, (0, 0, 0), 1, lineType)
    return image


def chonghe3(box1, bofinal):
    print('box1:')
    print(box1)
    print('bofinal:')
    print(bofinal)
    x01, y01, x02, y02 = box1
    x11, y11, x12, y12 = bofinal
    return


def mianji(box1, bofinal):
    print('canshu1:')
    print(box1)
    print('canshu2:')
    print(bofinal)

    # 方1
    x1, y1, final, y2 = box1
    x1, final = min(x1, final), max(x1, final)
    y1, y2 = min(y1, y2), max(y1, y2)

    # 方2
    x3, y3, x4, y4 = bofinal
    x3, x4 = min(x3, x4), max(x3, x4)
    y3, y4 = min(y3, y4), max(y3, y4)

    if (final <= x3 or x4 <= x1) and (y2 <= y3 or y4 <= y1):
        print(0)
    else:
        lens = min(final, x4) - max(x1, x3)
        wide = min(y2, y4) - max(y1, y3)
        print(lens)
        print(wide)
        print(lens * wide)

    print('--------------------------')


def chonghe(box1, bofinal):
    """bofinal落在了box1里"""
    x01, y01, box1w, box1h = box1
    x11, y11, bofinalw, bofinalh = bofinal

    x02 = x01 + box1w
    y02 = y01 + box1h
    x12 = x11 + bofinalw
    y12 = y11 + bofinalh

    if (x01 <= x11) and (y01 <= y12) and (x02 >= x12) and (y02 >= y12):
        print('True')
        return True
    else:
        print('False')
        return False
    print('--------------------------')


width = 600
# 生成一个空灰度图像
img = np.zeros((width, width, 3), np.uint8)
# 背景为白色
img[:, :, 0] = np.zeros([width, width]) + 255
img[:, :, 1] = np.ones([width, width]) + 254
img[:, :, 2] = np.ones([width, width]) * 255

fillColor = (0, 255, 0)
img = drawFillRect(img, 100, 18, 300, 300, fillColor)
box1 = (100, 18, 300, 300)

fillColor = (255, 0, 0)
img = drawFillRect(img, 200, 60, 100, 100, fillColor)
bofinal = (200, 60, 100, 100)
print('chonghe(box1, bofinal)')
chonghe(box1, bofinal)

fillColor = (0, 0, 255)
img = drawFillRect(img, 20, 30, 50, 50, fillColor)
box3 = (20, 30, 50, 50)
print('chonghe(box1, box3)')
chonghe(box1, box3)

fillColor = (0, 0, 255)
img = drawFillRect(img, 20, 200, 100, 100, fillColor)
box4 = (20, 200, 100, 100)
print('chonghe(box1, box4)')
chonghe(box1, box4)

fillColor = (0, 0, 255)
img = drawFillRect(img, 420, 200, 100, 100, fillColor)
box5 = (420, 200, 100, 100)
print('chonghe(box1, box5)')
chonghe(box1, box5)

fillColor = (0, 0, 255)
img = drawFillRect(img, 150, 350, 100, 100, fillColor)
box6 = (100, 300, 100, 100)
print('chonghe(box1, box6)')
chonghe(box1, box6)

# {'name': 'heijiang', 'x': 102, 'y': 18, 'width': 25, 'height': 24, 'score': 0.977899968624115}
# {'x': 8, 'y': 25, 'width': 12, 'height': 12}

cv.namedWindow("chess", cv.WINDOW_NORMAL)
cv.imshow('chess', img)
cv.waitKey()  # 显示 10000 ms 即 10s 后消失
cv.destroyAllWindows()
