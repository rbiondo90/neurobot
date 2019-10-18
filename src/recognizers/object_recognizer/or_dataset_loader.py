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
    imagePaths = sorted(list(paths.list_images(dataset_path)))
    if shuffle:
        # Usiamo un seed casuale
        random.seed(int(time.time() % 1000))
        random.shuffle(imagePaths)
    # loop sulle immagini di input
    count = 1
    for imagePath in imagePaths:
        # Carica l'immagine, la pre elabora e la memorizza nella lista di dati
        image = cv2.imread(imagePath)
        image = cv2.resize(image, im_size)
        image = img_to_array(image)
        data.append(image)
        # estrae le label dal path dell'imamgine e aggiorna la lista delle label
        label = imagePath.split(os.path.sep)[-2]
        print("Sto elaborando l'immagine %d di %d..." % (count, len(imagePaths)))
        if label == "item":
            label = 1
        else:
            label = 0
        labels.append(label)
        count += 1
    # Normalizziamo i valori dei pixel in modo da farli rientrare nell'intervallo [0,1]
    data = np.array(data, dtype="float") / 255.0
    labels = np.array(labels)
    return data, labels

