import numpy as np
import cv2
import pickle
import os
import random


def extract_features(image_path, alg):
    image = cv2.imread(image_path)

    try:
        kps, dsc = alg.detectAndCompute(image, None)
    except cv2.error as e:
        print('Error: ', e)
        return None

    return dsc

def batch_extractor(images_path, alg, pickled_db_path ):
    # pull images in image path
    files = [os.path.join(images_path, p) for p in sorted(os.listdir(images_path))]

    result = {}
    for f in files:
        print('Extracting features from image %s' % f)
        name = f.split('/')[-1].lower()
        result[name] = extract_features(f, alg)

    # saving all our feature vectors in pickled file
    with open(pickled_db_path, 'wb') as fp:
        pickle.dump(result, fp)

def main():
    # paths to the thumbnails and the test images
    thumbnail_path='./Pictures'
    test_path = './TestImages'

    # path to write pickled feature vectors. naming convention: {pictures, test}FV.pck
    picklePath = 'picturesKaze.pck'

    # all the keypoint descriptors
    kaze = cv2.KAZE_create()
    orb = cv2.ORB_create()
    akaze = cv2.AKAZE_create()
    brisk = cv2.BRISK_create()

    batch_extractor(images_path=thumbnail_path, alg=kaze, pickled_db_path='picturesKAZE.pck')
    batch_extractor(images_path=test_path, alg=kaze, pickled_db_path='testKAZE.pck')

    batch_extractor(images_path=thumbnail_path, alg=akaze, pickled_db_path='picturesAKAZE.pck')
    batch_extractor(images_path=test_path, alg=akaze, pickled_db_path='testAKAZE.pck')

    batch_extractor(images_path=thumbnail_path, alg=orb, pickled_db_path='picturesORB.pck')
    batch_extractor(images_path=test_path, alg=orb, pickled_db_path='testORB.pck')

    batch_extractor(images_path=thumbnail_path, alg=brisk, pickled_db_path='picturesBRISK.pck')
    batch_extractor(images_path=test_path, alg=brisk, pickled_db_path='testBRISK.pck')

main()
