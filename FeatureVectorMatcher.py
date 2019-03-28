

import numpy as np
import cv2 as cv
import os
import pickle
import scipy.spatial
import random
# from matplotlib import pyplot as plt

'''
# Initiate SIFT detector
kaze = cv.KAZE_create()

img1 = cv.imread('./testPictures/405testLight.JPG',0)          # queryImage

# find the keypoints and descriptors with SIFT
kp1, des1 = kaze.detectAndCompute(img1,None)

images_path = './pictures'
files = [os.path.join(images_path, p) for p in sorted(os.listdir(images_path))]
print(files)


mostKPsInCommon = -1
bestPicture = None
bestKPs = None
bestGood = None
bestIMG = None


for f in files:

    img2 = cv.imread(f,0)

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
    print(f + ": " + str(len(good)) + " matches")
    if len(good) > mostKPsInCommon:
        mostKPsInCommon = len(good)
        bestPicture = f
        bestIMG = img2
        bestKPs = kp2
        bestGood = good

print("Winner: " + bestPicture
'''

def singleCompare(testImg, pickled_db_path='picturesKAZE.pck'):
    print("unpickling")
    with open(pickled_db_path, 'rb') as fp:
        data = pickle.load(fp)
        thumbNames = []
        thumbMatrix = []
        for k, v in data.items():
            thumbNames.append(k)
            thumbMatrix.append(v)

        thumbMatrix = np.array(matrix)
        thumbNames = np.array(names)
    print("donepickling")

    mostKPsInCommon = -1
    bestPicture = None
    '''
    bestKPs = None
    bestGood = None
    bestIMG = None
    '''

    img1 = cv.imread(testImg,0)
    print('creating kaze')
    kaze = cv.KAZE_create()
    print('computing features')
    kp1, des1 = kaze.detectAndCompute(img1,None)
    bf = cv.BFMatcher()

    i = 0
    for des in matrix:

        matches = bf.knnMatch(des1,des, k=2)

        good = []
        for m,n in matches:
            if m.distance < 0.75*n.distance:
                good.append([m])

        print(names[i] + ': ' + str(len(good)))
        if len(good) > mostKPsInCommon:
            mostKPsInCommon = len(good)
            bestPicture = names[i]
            # bestIMG = img2
            # bestKPs = kp2
            # bestGood = good

        i = i + 1

    print("Winner: " + bestPicture)


def batchCompare(test_pck_path='testKAZE.pck', pictures_pck_path='picturesKAZE.pck'):
    print("unpickling test")
    with open(test_pck_path, 'rb') as fp:
        data = pickle.load(fp)
        testNames = []
        testMatrix = []
        for k, v in data.items():
            testNames.append(k)
            testMatrix.append(v)
        testMatrix = np.array(testMatrix)
        testNames = np.array(testNames)
    print("donepickling test")


    print("unpickling thumbnails")
    with open(pictures_pck_path, 'rb') as fp:
        data = pickle.load(fp)
        thumbNames = []
        thumbMatrix = []
        for k, v in data.items():
            thumbNames.append(k)
            thumbMatrix.append(v)

        thumbMatrix = np.array(thumbMatrix)
        thumbNames = np.array(thumbNames)
    print("donepickling thumbnails")

    j = 0
    bf = cv.BFMatcher()

    # create flann mathcer
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks=50)   # or pass empty dictionary
    flann = cv.FlannBasedMatcher(index_params,search_params)
    for testDes in testMatrix:
        mostKPsInCommon = -1
        bestPicture = None
        '''
        bestKPs = None
        bestGood = None
        bestIMG = None
        '''

        i = 0
        for thumbDes in thumbMatrix:
            matches = flann.knnMatch(testDes,thumbDes,k=2)

            good = []
            # ratio test as per Lowe's paper
            for k,(m,n) in enumerate(matches):
                if m.distance < 0.7*n.distance:
                    good.append([m])

            '''
            matches = bf.knnMatch(testDes,thumbDes, k=2)


            for m,n in matches:
                if m.distance < 0.75*n.distance:
                    good.append([m])
            '''


            if len(good) > mostKPsInCommon:
                mostKPsInCommon = len(good)
                bestPicture = thumbNames[i]
                # bestIMG = img2
                # bestKPs = kp2
                # bestGood = good

            i = i + 1

        print("Winner for " + testNames[j] +  ": " + bestPicture)

        j = j+1

batchCompare()

# img3 = cv.drawMatchesKnn(img1,kp1,bestIMG, bestKPs,bestGood,None,flags=2)
# plt.imshow(img3),plt.show()
