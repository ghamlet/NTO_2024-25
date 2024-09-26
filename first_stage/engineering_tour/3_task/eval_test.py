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


def check_need_connection(image: np.ndarray):
    """Проверка на нужный разъём зарядки"""

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_copy = gray.copy()

    mask = (gray >= 29) & (gray <= 29)
    gray_copy[mask] = 255 
    gray_copy[~mask] = 0  

    contours, _ = cv2.findContours(gray_copy, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    x_center, y_center, w, h = cv2.boundingRect(contours[0])





    ret, thresh = cv2.threshold(gray, 160, 255, cv2.THRESH_BINARY)
    

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


    charging_connectors = []
    for contour in contours:
        area = cv2.contourArea(contour) # находим площадь
        if 100 < area < 400:
            x, y, w, h = cv2.boundingRect(contour)  
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            charging_connectors.append([x, y, w, h])

    sort_charging_connectors = sorted(charging_connectors, key=lambda x: x[0])
    # print(sort_charging_connectors)


    cv2.imshow("gray_image", gray_copy)
    cv2.imshow("cut", thresh)

    if sort_charging_connectors[0][1] > y_center and sort_charging_connectors[1][1] < y_center and sort_charging_connectors[2][1] > y_center:
        return True
    else: return False


    
def find_red_circles(image):

    red_circles_coord = []
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv,(0, 165, 97), (40, 255, 195))
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        # x, y, w, h = cv2.boundingRect(contour)
        # cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        approx = cv2.approxPolyDP(contour, 0.2 * cv2.arcLength(contour, True), True) 
        
        cv2.drawContours(image, [contour], 0, (0, 0, 255), 5) 
    
        M = cv2.moments(contour) 
        if M['m00'] != 0.0: 
            x = int(M['m10']/M['m00']) 
            y = int(M['m01']/M['m00']) 
    
        if len(approx) == 3: 
            pass #убираем красные треугольнки
           
        else: 
            # cv2.putText(image, 'circle', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2) 
            red_circles_coord.append((x, y))

    # cv2.imshow("image", image)        
    # cv2.imshow("result", mask)

    return red_circles_coord



def predict_connect_number(image, img_list) -> int:
    # images = os.listdir("first_stage/engineering_tour/3_task/images")
    # for name_img in images:
    #     full_name = "first_stage/engineering_tour/3_task/images/" + name_img

    # image = cv2.imread(full_name)
    image = (cv2.resize(image, (1280, 720)))[:,100 :, :] #срез фото с 100 пикселя по икс

    coords = find_red_circles(image) #координаты центров красных кругов

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # cv2.imshow("gray_image", gray_image)
    
    ret, thresh = cv2.threshold(gray_image, 140, 255, cv2.THRESH_BINARY)

    thresh = ~thresh 
    # cv2.imshow("thresh", thresh)


    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


    centers_of_shapes = []
    for contour in contours:
        area = cv2.contourArea(contour) # находим площадь
        if area > 10000:
            x, y, w, h = cv2.boundingRect(contour)  # Получаем координаты и размеры
            centers_of_shapes.append( [x, y, w, h ]) #собираем иксы углов фигур чтобы в дальнейшем выстроить по возрастанию


    sort_centers_of_shapes = sorted(centers_of_shapes, key=lambda x: x[0]) #сортируем по иксу тобишь по порядковому расположению, ведь чем больше икс тем дальше находится обьект
    # print(sort_centers_of_shapes)
    for i, contour in enumerate(sort_centers_of_shapes):
        
        x, y, w, h = contour  # Получаем координаты и размеры
        for x_centr, y_centr in coords: #перебираем каждую координату из массива красных кругов и если ее центр окажется внутри границ прямоугольника то мы найдем позицию этой фигуры
            if (x < x_centr < (x+w )) and (y < y_centr <(y+h)):
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.circle(image, (x_centr, y_centr), 6, (255,0,0),-1)

                cut_image = image[y:y+h, x:x+w]
                if check_need_connection(cut_image):
                    right_number = i+1
    
                    cv2.putText(image, str(i+1), (x, y),   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2) 



    cv2.imshow("image", image)
    
    return right_number


predict_connect_number("first_stage/engineering_tour/3_task/images/IMG_20240823_164621.jpg", 0)
# find_red_circles()
