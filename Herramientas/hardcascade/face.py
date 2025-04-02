import cv2 as cv

rostro = cv.CascadeClassifier('./xmls/haarcascade_frontalface_alt.xml')
cap = cv.VideoCapture(0) #Para usar un video, cambia el 0 por la ruta del video
i = 0

while True:
    ret, frame = cap.read()
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    rostros = rostro.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in rostros:
        #frame = cv.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 2) #Comentar esta linea para quitar el rectangulo verde
        frame2 = frame[ y:y+h, x:x+w]
        frame2 = cv.resize(frame2, (100,100), interpolation=cv.INTER_AREA)
        if (i%15) == 0:    
            cv.imwrite('./images/personaH2'+str(i)+'.jpg', frame2)
        cv.imshow('rostro', frame2)
    cv.imshow('rostro', frame)
    i = i+1
    k = cv.waitKey(1)
    if k == 27:
        break
cap.release()
cv.destroyAllWindows()