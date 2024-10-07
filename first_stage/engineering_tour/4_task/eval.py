import cv2
import itertools
import math

import os
import numpy as np



def gradient(pt1,pt2):
    if (pt2[0] - pt1[0])==0:
        return 0
    return (pt2[1] - pt1[1]) / (pt2[0] - pt1[0])



def processing_frame(image):
    """"Находит контуры звёзд"""

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh, stars = cv2.threshold(gray, 12, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(stars, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    return contours


def find_Stars(contours):
    """"Находит координаты звезд и их размеры"""

    points = []
    areas = []
        
    for contour in contours:
        M = cv2.moments(contour)
        x = int(M["m10"] / M["m00"])
        y = int(M["m01"] / M["m00"])

        area = cv2.contourArea(contour) # размер звезды

        points.append([x, y])
        areas.append(area)

    areas = sorted(areas)
    return points, areas
   


def calc_angles(points) -> list:
    """Рассчитывает углы между тройками звезд"""

    angles = []
    radians = []
    combinations = list(itertools.permutations(points, 3))
    # print(combinations)

    for pt1, pt2, pt3 in combinations:
        try:
            m1 = gradient(pt1,pt2)
            m2 = gradient(pt1,pt3)
            angR = math.atan((m2 - m1) / (1+(m2*m1)))
           
           
            radians.append(angR)
        
            angD = round(math.degrees(angR))
            angles.append([angD, [pt1, pt2, pt3]])


        
        # print(angles)
        except:
            pass

    # print("Радианы ", sorted(radians))

    angles = sorted(angles, key=lambda x: x[0])
    return angles



def matching_galaxy(angles1: list, angles2: list, area_1, area_2) -> bool:
    """Сравнение созвездий"""


    num_of_angles_1 = len(angles1)
    num_of_angles_2 = len(angles2)

    if num_of_angles_1 != num_of_angles_2:  # если количество углов созвездий разное то количетво звезд в созвездиях разное т.е. это не одно и то же созвездие
        print("Количество звезд разное")
        return False

    
    else:
        if all(abs(angl1[0] - angl2[0]) <=3 for angl1, angl2 in zip(angles1, angles2)):  #[-87, [[178, 180], [85, 125], [146, 228]]]
            # парами по порядку берем углы из двух созвездий и сравниваем их, если одна из пар будет отличается более чем на 3 градуса, то углы разные, следовательнои озвездия разные
            if are_proportional(area_1, area_2):
                print("Звезды пропорциональны")
                return True
            else:
                print("Звезды не пропорциональны")
                return False

        # else: 
        #     return False


def is_mirror_reflection(angles1, angles2):
    uniq_x_1 = set()
    uniq_x_2 = set()

    uniq_y_1 = set()
    uniq_y_2 = set()


    for angle1 in angles1:

        for point in angle1[1]:
            uniq_x_1.add(point[0])

    for angle2 in angles2:

        for point in angle2[1]:
            uniq_x_2.add(point[0])


    
    for angle1 in angles1:

        for point in angle1[1]:
            uniq_y_1.add(point[1])

    for angle2 in angles2:

        for point in angle2[1]:
            uniq_y_2.add(point[1])


    if uniq_x_1 == uniq_x_2 or uniq_y_1 == uniq_y_2:
        print("Зеркало")
        return True
    else: return False



def are_proportional(list1, list2):


    # if list1 == [66.0, 96.0, 96.0, 130.0] and list2 == [23.0, 28.0, 29.5, 42.0]:
    #     return True

    # if list1 == [66.0, 96.0, 130.0] and list2 == [96.0, 130.0, 174.0]:
    #     return False
    
    
    relations = [x / y for x, y in zip(list1, list2)]
    average_relation = sum(relations) / len(relations)

    if all(abs(r - average_relation) < 0.2 for r in relations):
        return True

    else: return False



def is_same_stars(image1, image2):

    # cv2.imshow("galaxy_1", image1)
    # cv2.imshow("galaxy_2", image2)
    

    cnt1 = processing_frame(image1)
    pts1, area_1 = find_Stars(cnt1)
    # print("Площади_1: ",area_1)

    angl1 = calc_angles(pts1)

    # len_angl1 = len(angl1)
    # print("Углы1: ", angl1[len_angl1//2 :])

    cnt2 = processing_frame(image2)
    pts2 , area_2= find_Stars(cnt2)
    # print("Площади2: ",area_2)

    angl2 = calc_angles(pts2)
    # len_angl2 = len(angl2)
    # print("Углы2: ",angl2[len_angl2//2 :])


    if is_mirror_reflection(angl1, angl2):
        return False

    
    else:
        if matching_galaxy(angl1, angl2, area_1, area_2):
            return True
        else:
            return False


