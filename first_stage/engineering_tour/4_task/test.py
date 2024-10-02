import cv2
import itertools
import math

import os
import numpy as np



def gradient(pt1,pt2):
    if not(pt2[0] - pt1[0]):
        return 0
    return (pt2[1] - pt1[1]) / (pt2[0] - pt1[0])



def processing_frame(image):
    """"Находит контуры звёзд"""

    
    # image = cv2.imread(path)

    # if image[-5] == "1":
    #     cv2.imshow("galaxy_1", image)
    # else:
    #     cv2.imshow("galaxy_2", image)

    


    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh, stars = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
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

    combinations = list(itertools.permutations(points, 3))
    # print(combinations)

    for pt1, pt2, pt3 in combinations:

        m1 = gradient(pt1,pt2)
        m2 = gradient(pt1,pt3)
        angR = math.atan((m2 - m1) / (1+(m2*m1)))
        # radians.append(angR)
       
        angD = round(math.degrees(angR))
        angles.append(angD)


    angles = sorted(angles)
    # print(angles)

    return angles



def matching_galaxy(angles1: list, angles2: list, area_1, area_2) -> bool:
    """Сравнение созвездий"""


    print(area_1, area_2)
    relations = [S1 / S2 for S1, S2 in zip(area_1, area_2)]
    print(relations)

    average_relation = sum(relations) / len(relations)
    print(average_relation)

    if all(abs(r - average_relation) < 0.05 for r in relations):
        print("ghjkl")





    num_of_angles_1 = len(angles1)
    num_of_angles_2 = len(angles2)

    if num_of_angles_1 != num_of_angles_2:  # если количество углов созвездий разное то количетво звезд в созвездиях разное т.е. это не одно и то же созвездие
        return False

    

    if all(abs(angl1 - angl2) <=2 for angl1, angl2 in zip(angles1, angles2)):
        # парами по порядку берем углы из двух созвездий и сравниваем их, если одна из пар будет отличается более чем на 3 градуса, то углы разные, следовательнои озвездия разные
        return True



def is_same_stars(image1, image2):







# images = os.listdir("first_stage/engineering_tour/4_task/images")
# for image in images:

    # full_path_1 = "first_stage/engineering_tour/4_task/images/" + image[:-5] + "1" + ".jpg"
    # full_path_2 = "first_stage/engineering_tour/4_task/images/" + image[:-5] + "2" + ".jpg"

    

    cnt1 = processing_frame(image1)
    pts1, area_1 = find_Stars(cnt1)
    angl1 = calc_angles(pts1)

    cnt2 = processing_frame(image2)
    pts2 , area_2= find_Stars(cnt2)
    angl2 = calc_angles(pts2)

    

    if matching_galaxy(angl1, angl2, area_1, area_2):
        print(True)
    else: print(False)


    cv2.waitKey(0)




