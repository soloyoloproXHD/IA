import cv2 as cv

cap = cv.VideoCapture(0)

while True:
    ret, img = cap.read()
    if (ret):
        hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        cv.imshow('salida', img)
        cv.imshow('gris', hsv)
    k = cv.waitKey(1) & 0xFF
    if k == 27:
        break
        