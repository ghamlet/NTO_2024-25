# -*- coding: utf-8 -*-
import cv2
import numpy as np


def processing_red_cube(hsv_image, image):
    #выполняем действия для нахождения красного куба и его координат

    mask = cv2.inRange(hsv_image,(0,205,0),(255,255,255)) #маску создал с помощью трекбаров , находит верхнюю грань куба 

    #пиксели подходящего цвета останутся своего цвета а все остальные станут черными
    result = cv2.bitwise_and(image, image, mask=mask)

    gray_result = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    contours, _ = cv2.findContours(gray_result, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    max_area = 0
    for contour in contours:
        area = cv2.contourArea(contour) # находим площадь
        if area > max_area:
            max_area = area
            x, y, w, h = cv2.boundingRect(contour)  # Получаем координаты и размеры

    # cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    return x,y,w,h
    


def background_remov_and_obj_detect(hsv_image):
    #функция для удаления фона и нахождения координат всех обьектов на столе

    gray_image = cv2.cvtColor(hsv_image, cv2.COLOR_BGR2GRAY)

    # Определение промежутка фона в сером диапозоне
    lower_bound = 47 #47
    upper_bound = 80  #80

    #маска находит пиксели которые соответствуют диапозону
    mask = (gray_image >= lower_bound) & (gray_image <= upper_bound)
    gray_image[mask] = 0 # эти пиксели заменяем черными, т е фон станет черным
    gray_image[~mask] = 255  #инверсивная маска найдет оставшиеся пиксели т е те которые являются обьектами на столе

    # cv2.imshow("gray_image", gray_image)
    # cv2.waitKey(1)

    contours, _ = cv2.findContours(gray_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    obj_contrors = []
    max_area = 0
    for contour in contours:
        area = cv2.contourArea(contour) # находим площадь
        if area > 1000:
                
                """сейчас проблема в том что если несколько контуров находится """
            # if area > max_area:
            #     max_area = area
                #   # Фильтрация маленьких объектов
                obj_contrors.append(cv2.boundingRect(contour))
    print(obj_contrors)
    return obj_contrors


def size_comparison(hsv_image, image):
    #функция определяет размеры красного куба и другого обьекта и сравнивает их

    x_cube, y_cube, w_cube, h_cube = processing_red_cube(hsv_image, image)
    coords = background_remov_and_obj_detect(hsv_image)

    x_cube_mid = int(x_cube + w_cube /2)
    y_cube_mid = int(y_cube + h_cube /2)
    # cv2.circle(image, (x_cube_mid, y_cube_mid), 3, (255,255,0), 3)

    x_obj, y_obj, w_obj, h_obj = [None] *4
    for coord in coords:
        x1, y1, w, h = coord
        x2, y2 = x1 +w, y1 +h
        # cv2.circle(image, (x1, y1), 3, (255,255,0), 3)
        # cv2.circle(image, (x2, y2), 3, (255,255,0), 3)

        
        if not ((x1 < x_cube_mid < x2 ) and (y1 < y_cube_mid < y2)):
            x_obj, y_obj, w_obj, h_obj = coord

    # cv2.rectangle(image, (x_obj, y_obj), (x_obj + w_obj, y_obj + h_obj), (0, 255, 0), 2)

    if w_obj is None and h_obj is None:
        return True
    
    elif w_cube > w_obj and h_cube > h_obj:
        return True
    else: return False


def predict_ability_capture(image) -> bool:
    # image = cv2.resize(image, (1280, 720))
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    result = size_comparison(hsv_image, image)
    print(result)
    # cv2.imshow("res", image)
    

    # k = cv2.waitKey(0)
    
    return result


    