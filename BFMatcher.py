import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt


img1 = cv.imread('./pictures/405.jpg',0)          # queryImage
img2 = cv.imread('./testPictures/405testAskew.JPG',0) # trainImage
# Initiate KAZE detector
kaze = cv.KAZE_create()
# find the keypoints and descriptors with SIFT
kp1, des1 = kaze.detectAndCompute(img1,None)
kp2, des2 = kaze.detectAndCompute(img2,None)
# BFMatcher with default params
bf = cv.BFMatcher()
matches = bf.knnMatch(des1,des2, k=2)
# Apply ratio test
good = []
for m,n in matches:
    if m.distance < 0.75*n.distance:
        good.append([m])
# cv.drawMatchesKnn expects list of lists as matches.
print(len(good))
img3 = cv.drawMatchesKnn(img1,kp1,img2,kp2,good,None,flags=2)
plt.imshow(img3),plt.show()
