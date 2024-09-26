import cv2  
import numpy as np


def nothing(x):
    ...



def trackbar(minblue=0, mingreen=0, minred=0, maxblue=255, maxgreen=255, maxred=255):
    # создание трекеров для каждого цвета

    cv2.namedWindow( "Trackbar")
    cv2.createTrackbar('minb', 'Trackbar', minblue, 255, nothing)
    cv2.createTrackbar('ming', 'Trackbar', mingreen, 255, nothing)
    cv2.createTrackbar('minr', 'Trackbar', minred, 255, nothing)
    cv2.createTrackbar('maxb', 'Trackbar', maxblue, 255, nothing)
    cv2.createTrackbar('maxg', 'Trackbar', maxgreen, 255, nothing)
    cv2.createTrackbar('maxr', 'Trackbar', maxred, 255, nothing)


# trackbar()

image = cv2.imread("first_stage/engineering_tour/3_task/cut_red.png")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(gray, 160, 255, cv2.THRESH_BINARY)

contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

x_c, y_c = None, None

charging_connectors = []
for contour in contours:
    area = cv2.contourArea(contour) # находим площадь
    print(area)
    if 100 < area < 400:
        x, y, w, h = cv2.boundingRect(contour)  
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        charging_connectors.append([x, y, w, h])

sort_charging_connectors = sorted(charging_connectors, key=lambda x: x[0])
print(sort_charging_connectors)

if sort_charging_connectors[0][1] > y_c and sort_charging_connectors[1][1] < y_c and sort_charging_connectors[2][1] > y_c:
    print(True)

    
# for connector in sort_charging_connectors:
#     x, y, w, h = connector
#     if 


# while True:
    
#     minb = cv2.getTrackbarPos('minb', 'Trackbar')
#     ming = cv2.getTrackbarPos('ming', 'Trackbar')
#     minr = cv2.getTrackbarPos('minr', 'Trackbar')
#     maxb = cv2.getTrackbarPos('maxb', 'Trackbar')
#     maxg = cv2.getTrackbarPos('maxg', 'Trackbar')
#     maxr = cv2.getTrackbarPos('maxr', 'Trackbar')

#     # применяем пороги цветов
#     mask = cv2.inRange(hsv,(minb,ming,minr),(maxb,maxg,maxr))

#     #пиксели подходящего цвета останутся своего цвета а все остальные станут черными
#     result = cv2.bitwise_and(image, image, mask=mask)


cv2.imshow('result', image)

k = cv2.waitKey(0)
# при нажатии на клавишу q программа завершитс