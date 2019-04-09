import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt


img1 = cv.imread('./TestImages/3044.jpg',0)          # queryImage
img2 = cv.imread('./Pictures/3227.jpg',0) # trainImage
# Initiate KAZE detector
alg = cv.BRISK_create()
# find the keypoints and descriptors with SIFT
kp1, des1 = alg.detectAndCompute(img1,None)
kp2, des2 = alg.detectAndCompute(img2,None)
# BFMatcher with default params
FLANN_INDEX_LSH = 6
index_params= dict(algorithm = FLANN_INDEX_LSH,
               table_number = 6, # 12
               key_size = 12,     # 20
               multi_probe_level = 1) #2
search_params = dict(checks=50)   # or pass empty dictionary
flann = cv.FlannBasedMatcher(index_params,search_params)

matches = flann.knnMatch(des1,des2,k=2)

# bf = cv.BFMatcher(norm=cv.NORM_HAMMING,cross_check=true)
# matches = bf.knnMatch(des1,des2, k=2)
# Apply ratio test
good = []
for match in matches:
    if len(match) > 1:
        m = match[0] ; n = match[1]
        if m.distance < 0.75*n.distance:
            good.append([m])
# cv.drawMatchesKnn expects list of lists as matches.
print(len(good))
img3 = cv.drawMatchesKnn(img1,kp1,img2,kp2,good,None,flags=2)
plt.imshow(img3),plt.show()
