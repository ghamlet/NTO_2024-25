import cv2

import numpy as np



image1 = cv2.imread('first_stage/engineering_tour/4_task/images/xP6ptq-qJT-XjV-I1NzWM-1.jpg')
image2 = cv2.imread('first_stage/engineering_tour/4_task/images/xP6ptq-qJT-XjV-I1NzWM-2.jpg')

# image1 = cv2.imread('first_stage/engineering_tour/4_task/images/PxoA3p-o6T-LDB-UEqZG0-1.jpg')
# image2 = cv2.imread('first_stage/engineering_tour/4_task/images/PxoA3p-o6T-LDB-UEqZG0-2.jpg')


gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

gray1 = cv2.GaussianBlur(gray1, (5, 5), 0)
gray2 = cv2.GaussianBlur(gray2, (5, 5), 0)


thresh1, stars1 = cv2.threshold(gray1, 127, 255, cv2.THRESH_BINARY)
thresh2, stars2 = cv2.threshold(gray2, 127, 255, cv2.THRESH_BINARY)

contours1, _ = cv2.findContours(stars1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours2 , _= cv2.findContours(stars2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


def extract_star_features(contour):
    M = cv2.moments(contour)
    cx = int(M["m10"] / M["m00"])
    cy = int(M["m01"] / M["m00"])
    area = cv2.contourArea(contour)
    orientation = cv2.minAreaRect(contour)[-1]
    return cx, cy, area, orientation

star_features1 = [extract_star_features(c) for c in contours1]
star_features2 = [extract_star_features(c) for c in contours2]


def star_distance(f1, f2):
    cx1, cy1, area1, o1 = f1
    cx2, cy2, area2, o2 = f2
    dist = np.sqrt((cx1 - cx2)**2 + (cy1 - cy2)**2) + abs(area1 - area2) + abs(o1 - o2)
    return dist

matches = []
for f1 in star_features1:
    min_dist = float("inf")
    min_f2 = None
    for f2 in star_features2:
        dist = star_distance(f1, f2)
        if dist < min_dist:
            min_dist = dist
            min_f2 = f2
    if min_dist < 200:
        matches.append((f1, min_f2))


def estimate_transform(matches):
    src_pts = np.float32([f1[:2] for f1, _ in matches])
    dst_pts = np.float32([f2[:2] for _, f2 in matches])
    M, _ = cv2.estimateAffinePartial2D(src_pts, dst_pts)
    scale = np.sqrt(M[0, 0]**2 + M[1, 0]**2)
    angle = np.arctan2(M[1, 0], M[0, 0]) * 180 / np.pi
    return scale, angle

scale, angle = estimate_transform(matches)
print(scale, angle)


if abs(scale - 1.0) < 100 and abs(angle) < 100:
    print("Constellations are the same.")
else:
    print("Constellations are different.")
