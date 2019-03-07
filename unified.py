import cv2
import numpy as np
from imageio import imread
import pickle
import os
import scipy.spatial
import random
import matplotlib.pyplot as plt

def extract_features(image_path, vector_size=32):
    image = imread(image_path)

    try:
        alg = cv2.KAZE_create()
        kps, dsc = alg.detectAndCompute(image, None)
        '''
        dsc = dsc.flatten()
        needed_size = (vector_size * 64)
        if dsc.size < needed_size:
                dsc = np.concatenate([dsc, np.zeros(needed_size - dsc.size)])
        '''
    except cv2.error as e:
        print('Error: ', e)
        return None

    return dsc

def batch_extractor(images_path, pickled_db_path="features.pck"):
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

class Matcher(object):

    def __init__(self, pickled_db_path="features.pck"):
        with open(pickled_db_path, 'rb') as fp:
            self.data = pickle.load(fp)
        self.names = []
        self.matrix = []
        for k, v in self.data.items():
            self.names.append(k)
            self.matrix.append(v)
        self.matrix = np.array(self.matrix)
        self.names = np.array(self.names)

    def cos_cdist(self, vector):
        # getting cosine distance between search image and images database
        v = vector.reshape(1, -1)
        return scipy.spatial.distance.cdist(self.matrix, v, 'cosine').reshape(-1)

    def match(self, image_path, topn=5):
        features = extract_features(image_path)
        img_distances = self.cos_cdist(features)
        # getting top 5 records
        nearest_ids = np.argsort(img_distances)[:topn].tolist()
        nearest_img_paths = self.names[nearest_ids].tolist()

        return nearest_img_paths, img_distances[nearest_ids].tolist()

def show_img(path):
    img = imread(path)
    plt.imshow(img)
    plt.show()

def run():
    images_path = './pictures'
    test_images_path = './testPictures'
    files = [os.path.join(images_path, p) for p in sorted(os.listdir(images_path))]
    test_files = [os.path.join(test_images_path, p) for p in sorted(os.listdir(test_images_path))]
    # getting 3 random images
    sample = random.sample(test_files, 5)

    # batch_extractor(images_path, pickled_db_path="features.pck")

    ma = Matcher('features.pck')

    for s in sample:
        print('Query image ==========================================')
        show_img(s)
        names, match = ma.match(s, topn=1)
        print('Result images ========================================')
        for i in range(1):
            # we got cosine distance, less cosine distance between vectors
            # more they similar, thus we subtruct it from 1 to get match value
            print('Match %s' % (1-match[i]))
            show_img(os.path.join(images_path, names[i]))

run()
