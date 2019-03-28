import numpy as np
import cv2
import pickle
import os
import scipy.spatial
import random
from matplotlib import pyplot as plt

def extract_features(image_path, vector_size=32):
    image = cv2.imread(image_path)

    try:
        alg = cv2.KAZE_create()
        kps, dsc = alg.detectAndCompute(image, None)
    except cv2.error as e:
        print('Error: ', e)
        return None

    return dsc

def batch_extractor(images_path, pickled_db_path="picturesKAZE.pck"):
    # pull images in image path
    files = [os.path.join(images_path, p) for p in sorted(os.listdir(images_path))]

    result = {}
    for f in files:
        print('Extracting features from image %s' % f)
        name = f.split('/')[-1].lower()
        result[name] = extract_features(f)

    # saving all our feature vectors in pickled file
    with open(pickled_db_path, 'wb') as fp:
        pickle.dump(result, fp)

def main():
    imagesPath='./Thumbnails/pictures'
    picklePath = 'picturesKaze.pck'
    batch_extractor(images_path=imagesPath, pickled_db_path=picklePath)

main()
