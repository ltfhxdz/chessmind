# -*- coding: utf-8 -*-
import cv2

image = cv2.imread('D:/xyz/workspace/chessmind/chess/data/images/chess1.jpg')
width = image.shape[0]
height = image.shape[1]
print(height)
print(width)
# resizeImg = cv2.resize(image, (int(width / 2), int(height / 2)), interpolation=cv2.INTER_AREA)
resizeImg = cv2.resize(image, (230, 290), interpolation=cv2.INTER_AREA)
cv2.imshow('original', image)
cv2.imshow('resize', resizeImg)
cv2.imwrite('D:/xyz/workspace/chessmind/chess/data/images/test/chess1_3.jpg', resizeImg)
cv2.waitKey(0)
