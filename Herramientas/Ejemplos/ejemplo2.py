import cv2 as cv
import numpy as np

img = cv.imread("./images/manzana.jpg")
hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

ub=np.array([0, 120, 40])
ua=np.array([10, 255, 255])

ub1=np.array([170, 40, 40])
ua1=np.array([180, 255, 255])

mask = cv.inRange(hsv, ub, ua)
mask1 = cv.inRange(hsv, ub1, ua1)

maskf = mask + mask1 
result = cv.bitwise_and(img, img, mask=maskf)

cv.imshow('hsv', hsv)
cv.imshow('mask', mask)
cv.imshow('result', result)

cv.waitKey()
