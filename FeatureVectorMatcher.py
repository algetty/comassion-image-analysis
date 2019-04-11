

import numpy as np
import cv2 as cv
import os
import pickle
import scipy.spatial
import random
from timeit import default_timer as timer

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


def batchCompare(test_pck_path, pictures_pck_path, file, hamming=False):
    f = open(file, 'w')

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
    if hamming:
        FLANN_INDEX_LSH = 6
        index_params= dict(algorithm = FLANN_INDEX_LSH,
                       table_number = 6, # 12
                       key_size = 12,     # 20
                       multi_probe_level = 1) #2
    else:
        # create flann mathcer
        FLANN_INDEX_KDTREE = 1
        index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)

    search_params = dict(checks=50)   # or pass empty dictionary
    flann = cv.FlannBasedMatcher(index_params,search_params)
    for testDes in testMatrix:
        mostKPsInCommon = -1
        bestPicture = None

        i = 0
        for thumbDes in thumbMatrix:
            good = []
            if not thumbDes is None and not testDes is None:

                matches = flann.knnMatch(testDes,thumbDes,k=2)

                for match in matches:
                    if len(match) > 1:
                        m = match[0] ; n = match[1]
                        if m.distance < 0.75*n.distance:
                            good.append([m])


            if len(good) > mostKPsInCommon:
                mostKPsInCommon = len(good)
                bestPicture = thumbNames[i]

            i = i + 1



        if testNames[j] == bestPicture:
            k=1
        else:
            k=0
        # print(testNames[j] +  "," + bestPicture + ", " + str(k))
        f.write(testNames[j] +  "," + bestPicture + ", " + str(k))

        j = j+1
    f.close()

if __name__=='__main__':
    start_time = timer()
    batchCompare('testKAZE.pck', 'picturesKAZE.pck', 'KAZEoutput.csv',hamming=False)
    end_time = timer()
    time = end_time - start_time
    print("time to run kaze: " + str(time))

    start_time = timer()
    batchCompare('testORB.pck', 'picturesORB.pck', 'ORBoutput.csv',hamming=True)
    end_time = timer()
    time = end_time - start_time
    print("time to run orb: " + str(time))

    start_time = timer()
    batchCompare('testAKAZE.pck', 'picturesAKAZE.pck', 'AKAZEoutput.csv', hamming=True)
    end_time = timer()
    time = end_time - start_time
    print("time to run akaze: " + str(time))

    start_time = timer()
    batchCompare('testBRISK.pck', 'picturesBRISK.pck', 'BRISKoutput.csv', hamming=True)
    end_time = timer()
    time = end_time - start_time
    print("time to run brisk: " + str(time))
