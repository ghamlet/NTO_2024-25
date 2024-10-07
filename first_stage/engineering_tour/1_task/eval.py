# -*- coding: utf-8 -*-
import cv2
import numpy as np
# TODO: Допишите импорт библиотек, которые собираетесь использовать


def predict_illumination(image) -> bool:
    """
        Функция для определения возможности ориентироваться по изображению.

        Входные данные: изображение (bgr), прочитано cv2.imread
        Выходные данные: True или False
                         True - по изображениею можно ориентироваться
                         False - изображение засвечено, по нему нельзя ориентироваться

        Примеры вывода:
            True
            False
    """
    # TODO: Отредактируйте эту функцию по своему усмотрению.
    # Вы можете создавать собственные функции в этом файле, но все они должны вызываться внутри функции predict_illumination.

    brightness_threshold=240
    pixel_ratio_threshold=0.05
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Вычисление среднего значения яркости
    average_brightness = np.mean(gray_image)

    # Подсчет количества пикселей с яркостью выше порога
    bright_pixels_count = np.sum(gray_image > brightness_threshold)
    total_pixels = gray_image.size

    # Процент пикселей с яркостью выше порога
    bright_pixel_ratio = bright_pixels_count / total_pixels

    # Оценка изображения
    if bright_pixel_ratio > pixel_ratio_threshold:
        result = False
    else:
        result = True
    return result