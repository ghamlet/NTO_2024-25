# -*- coding: utf-8 -*-
import cv2
import numpy as np


def load_images():
    """ 
        Функция осуществляет загрузку эталонных изображений из файла(ов).
        Если вы не собираетесь использовать эту функцию, пусть возвращает пустой список []
        Если вы используете несколько изображений, то возвращайте их списком [img1, img2, ...]

        То, что вы вернёте из этой функции, будет передано вторым аргументом в функцию predict_connect_number
    """

    img_list = []
    return img_list



def check_need_connection(image: np.ndarray):
    """Проверка на нужный разъём зарядки"""

#--------------------------------------------
    #блок в котором мы находим координату центра круглого разьема путем нахождения маленькой синей окружности нарисованной ранее в центре
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_copy = gray.copy()         #копию серого изображения используем для нахождения центра
    #а оригинал серого изображения для посика координат белых коннекторов

    mask = (gray >= 29) & (gray <= 29) #значение синего цвета в сером диапозоне
    gray_copy[mask] = 255               #найденные синие пиксели заменяем на белые чтобы использовать потом функцию findContours
    gray_copy[~mask] = 0                 # все остальные пиксели станут черными

    contours, _ = cv2.findContours(gray_copy, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    x_center, y_center, w, h = cv2.boundingRect(contours[0])
    #т к контур состоящий из чистых синих пикселей будет один то берем первым и единственный контур
#--------------------------------------------------------

    #блок где находим координаты торчащих коннекторов, которые представляют из себя белые окружности
    ret, thresh = cv2.threshold(gray, 160, 255, cv2.THRESH_BINARY)  #пиксели до 160 в сером диапозоне станут черными, а нужные нам белые коннекторы останутся белыми
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    charging_connectors = []   #массив для хранения размеров прямоугольников описанных вокруг коннекторов
    for contour in contours:
        area = cv2.contourArea(contour) # находим площадь контура
        if 100 < area < 400:           # фильтруем контур от помех
            x, y, w, h = cv2.boundingRect(contour)  
            # cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            charging_connectors.append([x, y, w, h])

    sort_charging_connectors = sorted(charging_connectors, key = lambda list_: list_[0])
    #сортируем контуры по возрастанию координаты x 

    # cv2.imshow("gray_image", gray_copy)
    # cv2.imshow("cut", thresh)

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
            try:
            # cv2.putText(image, 'circle', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2) 
                red_circles_coord.append((x, y))
            except:
                pass

    # cv2.imshow("image", image)        
    # cv2.imshow("result", mask)

    return red_circles_coord



def predict_connect_number(image, img_list) -> int:
    try:
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

        right_number = None
        for i, contour in enumerate(sort_centers_of_shapes):
            
            x, y, w, h = contour  # Получаем координаты и размеры
            for x_centr, y_centr in coords: #перебираем каждую координату из массива красных кругов и если ее центр окажется внутри границ прямоугольника то мы найдем позицию этой фигуры
                if (x < x_centr < (x+w )) and (y < y_centr <(y+h)):
                    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.circle(image, (x_centr, y_centr), 6, (255,0,0),-1)

                    cut_image = image[y:y+h, x:x+w]
                    if check_need_connection(cut_image):
                        right_number = i+1
                        return right_number
        
                        # cv2.putText(image, str(i+1), (x, y),   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2) 

    except:
        pass

    # cv2.imshow("image", image)
    
    # return right_number


