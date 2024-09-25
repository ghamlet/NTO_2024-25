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





def find_red_circles(image):

    red_circles_coord = []
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv,(0, 165, 97), (40, 255, 195))
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.2 * cv2.arcLength(contour, True), True) 
        
        cv2.drawContours(image, [contour], 0, (0, 0, 255), 5) 
    
        M = cv2.moments(contour) 
        if M['m00'] != 0.0: 
            x = int(M['m10']/M['m00']) 
            y = int(M['m01']/M['m00']) 
    
        if len(approx) == 3: 
            pass #убираем красные треугольнки
           
        else: 
            cv2.putText(image, 'circle', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2) 
            red_circles_coord.append((x, y))

    cv2.imshow("image", image)        
    cv2.imshow("result", mask)

    return red_circles_coord



def predict_connect_number(image, img_list) -> int:
    images = os.listdir("first_stage/engineering_tour/3_task/images")
    for name_img in images:
        full_name = "first_stage/engineering_tour/3_task/images/" + name_img

        image = cv2.imread(full_name)
        image = (cv2.resize(image, (1280, 720)))[:,100 :, :] #срез фото с 100 пикселя по икс

        coords = find_red_circles(image) #координаты центров красных кругов

        # hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        cv2.imshow("gray_image", gray_image)
        


        ret, thresh = cv2.threshold(gray_image, 140, 255, cv2.THRESH_BINARY)

        thresh = ~thresh 
        cv2.imshow("thresh", thresh)


        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


        centers_of_shapes = []
        for contour in contours:
            area = cv2.contourArea(contour) # находим площадь
            if area > 10000:
                x, y, w, h = cv2.boundingRect(contour)  # Получаем координаты и размеры
                centers_of_shapes.append( [x, y, w, h ]) #собираем иксы углов фигур чтобы в дальнейшем выстроить по возрастанию


        sort_centers_of_shapes = sorted(centers_of_shapes, key=lambda x: x[0]) #сортируем по иксу тобишь по порядковому расположению, ведь чем больше икс тем дальше находится обьект
        print(sort_centers_of_shapes)
        for i, contour in enumerate(sort_centers_of_shapes):
            
            x, y, w, h = contour  # Получаем координаты и размеры
            for coord in coords: #перебираем каждую координату из массива красных кругов и если ее центр окажется внутри границ прямоугольника то мы найдем позицию этой фигуры
                if (x < coord[0] < (x+w )) and (y < coord[1] <(y+h)):
                    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(image, str(i+1), (x, y),   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2) 
    


        cv2.imshow("image", image)

        cv2.waitKey(0)


predict_connect_number("first_stage/engineering_tour/3_task/images/IMG_20240823_164621.jpg", 0)
# find_red_circles()
