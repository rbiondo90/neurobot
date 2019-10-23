import os
import random
import time

import cv2
from imutils import paths
from keras_preprocessing.image import img_to_array
import numpy as np

import defaults

DEFAULT_DATASET_DIRECTORY = os.path.join(defaults.DATASETS_DIRECTORY, "item_no_item_dataset")
def load_dataset(dataset_path=DEFAULT_DATASET_DIRECTORY, im_size = (128,128), shuffle=True):
    data = []
    labels = []
    # Prende le immagini dalle directory e (se shuffle e' true) le mischia casualmente
    image_paths = sorted(list(paths.list_images(dataset_path)))
    if shuffle:
        # Usiamo un seed casuale
        random.seed(int(time.time() % 1000))
        random.shuffle(image_paths)
    # loop sulle immagini di input
    count = 1
    for image_path in image_paths:
        print("Sto elaborando l'immagine %d di %d..." % (count, len(image_paths)))
        data.append(prepare_image(image_path, im_size))
        labels.append(get_label(image_path))
        count += 1
    labels = np.array(labels)
    data = np.array(data)
    return data, labels

def prepare_image(im_path, im_size):
    image = cv2.imread(im_path)
    image = cv2.resize(image, im_size)
    return np.array(image, dtype="float") / 255.0

def get_label(im_path):
    if im_path.split(os.path.sep)[-2] == "item":
        return 1
    else:
        return 0

if __name__ == '__main__':
    data, labels = load_dataset()
    print("Dataset caricato")

