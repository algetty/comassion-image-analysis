

import numpy as np
import cv2 as cv
import os
import pickle
import scipy.spatial
import random
from timeit import default_timer as timer

'''
    Search for all the images in test_pck_path in pictures_pck_path

    file is the output file
    hamming is a boolean for hamming or euclidean distance
'''
def batch_compare(test_pck_path, pictures_pck_path, file, hamming=False):
    f = open(file, 'w')

    print("unpickling test")
    with open(test_pck_path, 'rb') as fp:
        data = pickle.load(fp)
        test_names = []
        test_matrix = []
        for k, v in data.items():
            test_names.append(k)
            test_matrix.append(v)
        test_matrix = np.array(test_matrix)
        test_names = np.array(test_names)
    print("donepickling test")


    print("unpickling thumbnails")
    with open(pictures_pck_path, 'rb') as fp:
        data = pickle.load(fp)
        thumb_names = []
        thumb_matrix = []
        for k, v in data.items():
            thumb_names.append(k)
            thumb_matrix.append(v)

        thumb_matrix = np.array(thumb_matrix)
        thumb_names = np.array(thumb_names)
    print("donepickling thumbnails")


    if hamming:
        FLANN_INDEX_LSH = 6
        index_params= dict(algorithm = FLANN_INDEX_LSH,
                       table_number = 6,
                       key_size = 12,
                       multi_probe_level = 1)
    else:
        FLANN_INDEX_KDTREE = 1
        index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)

    search_params = dict(checks=50)
    # flann implements approximate nearest neighbor search
    flann = cv.FlannBasedMatcher(index_params,search_params)

    j = 0
    for test_des in test_matrix:
        most_kps_in_common = -1
        best_picture = None

        i = 0
        for thumb_des in thumb_matrix:
            good = []
            if not thumb_des is None and not test_des is None:

                matches = flann.knnMatch(test_des,thumb_des,k=2)

                for match in matches:
                    if len(match) > 1:
                        m = match[0] ; n = match[1]
                        if m.distance < 0.75*n.distance:
                            good.append([m])


            if len(good) > most_kps_in_common:
                most_kps_in_common = len(good)
                best_picture = thumb_names[i]

            i = i + 1


        # k=1 means 1 success. this also easy counting of successful runs
        if test_names[j] == best_picture:
            k=1
        else:
            k=0
        # print(test_names[j] +  "," + best_picture + ", " + str(k))
        f.write(test_names[j] +  "," + best_picture + ", " + str(k))

        j = j+1
    f.close()

if __name__=='__main__':
    start_time = timer()
    batch_compare('testKAZE.pck', 'picturesKAZE.pck', 'KAZEoutput.csv',hamming=False)
    end_time = timer()
    time = end_time - start_time
    print("time to run kaze: " + str(time))

    start_time = timer()
    batch_compare('testORB.pck', 'picturesORB.pck', 'ORBoutput.csv',hamming=True)
    end_time = timer()
    time = end_time - start_time
    print("time to run orb: " + str(time))

    start_time = timer()
    batch_compare('testAKAZE.pck', 'picturesAKAZE.pck', 'AKAZEoutput.csv', hamming=True)
    end_time = timer()
    time = end_time - start_time
    print("time to run akaze: " + str(time))

    start_time = timer()
    batch_compare('testBRISK.pck', 'picturesBRISK.pck', 'BRISKoutput.csv', hamming=True)
    end_time = timer()
    time = end_time - start_time
    print("time to run brisk: " + str(time))
