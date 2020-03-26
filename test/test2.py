# -*- coding: UTF-8 -*-
import cv2 as cv
import numpy as np

width = 1000
img = np.zeros((width, width, 3), np.uint8)  # 生成一个空灰度图像
img[:, :, 0] = np.zeros([width, width]) + 255
img[:, :, 1] = np.ones([width, width]) + 254
img[:, :, 2] = np.ones([width, width]) * 255

x = round(101.000056)
print(x)

height = 96
# left = 313
left = 312
top = 165
width = 106
avg = (width + height)/2
print('left+width='+str(left)+'+'+str(avg)+'='+str(avg))
print('top+height='+str(top)+'+'+str(avg)+'='+str(avg))
ptLeftTop = (left, top)  # left,top
ptRightBottom = (left+width, top+height)  # left+width,top+height
thickness = 1
lineType = 4
blue = (255, 0, 0)
cv.rectangle(img, ptLeftTop, ptRightBottom, blue, thickness, lineType)
cv.namedWindow("chess", cv.WINDOW_NORMAL)
cv.imshow('chess', img)
cv.waitKey()  # 显示 10000 ms 即 10s 后消失
cv.destroyAllWindows()
