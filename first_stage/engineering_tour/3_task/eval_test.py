# -*- coding: utf-8 -*-
import cv2
import numpy as np
import os

def load_images():
    """ 
        Функция осуществляет загрузку эталонных изображений из файла(ов).
        Если вы не собираетесь использовать эту функцию, пусть возвращает пустой список []
        Если вы используете несколько изображений, то возвращайте их списком [img1, img2, ...]

        То, что вы вернёте из этой функции, будет передано вторым аргументом в функцию predict_connect_number
    """

    img_list = []

    # TODO: Отредактируйте функцию по своему усмотрению.
    # Эталонные изображения вместе с файлом "eval.py" поместите в архив и загрузите на онлайн платформу в качестве решения.

    # Пример загрузки изображений из файлов
    # img1 = cv2.imread("Etalon1.png")
    # img_list.append(img1)
    # ....

    return img_list


def predict_connect_number(image, img_list) -> int:
    images = os.listdir("first_stage/engineering_tour/3_task/images")
    
    
    template = cv2.imread('first_stage/engineering_tour/3_task/pat.png')
    hsv = cv2.cvtColor(template, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(hsv, cv2.COLOR_BGR2GRAY)

    w, h= gray.shape[::-1]


    # Определение промежутка фона в сером диапозоне
    lower_bound = 42 #47
    upper_bound = 80  #80

    #маска находит пиксели которые соответствуют диапозону
    mask = (gray >= lower_bound) & (gray <= upper_bound)
    gray[mask] = 0 # эти пиксели заменяем черными, т е фон станет черным
    gray[~mask] = 255
    cv2.imshow("gray", gray)
    cv2.waitKey(0)





    for name_img in images:
        full_name = "first_stage/engineering_tour/3_task/images/" + name_img

        image = cv2.imread(full_name)
        image = cv2.resize(image, (1280, 720))
        

        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        gray_image = cv2.cvtColor(hsv_image, cv2.COLOR_BGR2GRAY)
        cv2.imshow("gray_image", gray_image)


        # Определение промежутка фона в сером диапозоне
        lower_bound = 42 #47d
        upper_bound = 80  #80

        #маска находит пиксели которые соответствуют диапозону
        mask = (gray_image >= lower_bound) & (gray_image <= upper_bound)
        gray_image[mask] = 0 # эти пиксели заменяем черными, т е фон станет черным
        gray_image[~mask] = 255  #инверсивная маска найдет оставшиеся пиксели т е те которые являются обьектами на столе


        res = cv2.matchTemplate(gray_image, gray, cv2.TM_CCOEFF_NORMED)
        threshold = 0.4
        loc = np.where(res >= threshold)
        print(loc)
        x, y = loc[1], loc[0]
        for (xt, yt) in zip(x, y):
            cv2.rectangle(image, (xt, yt), (xt + w, yt + h), (0, 0, 255), 2)

        cv2.imshow("black", image)
        cv2.waitKey(0)
predict_connect_number("first_stage/engineering_tour/3_task/images/IMG_20240823_164621.jpg", 0)