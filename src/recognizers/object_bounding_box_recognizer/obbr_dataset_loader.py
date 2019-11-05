#%%
import os
import random
import time
import cv2
from imutils import paths
from keras_preprocessing.image import img_to_array
import numpy as np
from xml.dom import minidom
from recognizers.object_recognizer import or_dataset_loader
from utils.generic import defaults

DEFAULT_IMAGE_DIRECTORY = os.path.join(or_dataset_loader.DEFAULT_DATASET_DIRECTORY, "item")
DEFAULT_BOXES_DIRECTORY = os.path.join(defaults.DATASETS_DIRECTORY, "item_boxes_dataset")

def load_dataset(image_directory = DEFAULT_IMAGE_DIRECTORY, boxes_directory = DEFAULT_BOXES_DIRECTORY,
                 im_size = (128,128), shuffle=True):
    def get_box(image_path):
        box_path = os.path.join(boxes_directory, os.path.splitext(os.path.basename(image_path))[0] + ".xml")
        xml_file = minidom.parse(box_path)
        xmin = int(xml_file.getElementsByTagName("xmin")[0].firstChild.data)
        xmax = int(xml_file.getElementsByTagName("xmax")[0].firstChild.data)
        ymin = int(xml_file.getElementsByTagName("ymin")[0].firstChild.data)
        ymax = int(xml_file.getElementsByTagName("ymax")[0].firstChild.data)
        return [xmin, xmax, ymin, ymax]
    data = []
    boxes = []
    image_paths = sorted(list(paths.list_images(image_directory)))
    if shuffle:
        # Usiamo un seed casuale
        random.seed(int(time.time() % 1000))
        random.shuffle(image_paths)
    # loop sulle immagini di input
    count = 1
    for image_path in image_paths:
        try:
            # Carica l'immagine, la pre elabora e la memorizza nella lista di dati
            print("Sto elaborando l'immagine %d di %d..." % (count, len(image_paths)))
            image = cv2.imread(image_path)
            # normalization_factor_x = 128./image.shape[1]
            # normalization_factor_y = 128./image.shape[0]
            box = get_box(image_path)
            # box[0] *= normalization_factor_x
            # box[1] *= normalization_factor_x
            # box[2] *= normalization_factor_y
            # box[3] *= normalization_factor_y
            box[0] = float(box[0]) / image.shape[1]
            box[1] = float(box[1]) / image.shape[1]
            box[2] = float(box[2]) / image.shape[0]
            box[3] = float(box[3]) / image.shape[0]
            boxes.append(box)
            image = cv2.resize(image, im_size)
            image = img_to_array(image)
            data.append(image)
        except:
            continue
        finally:
            count += 1
    # Normalizziamo i valori dei pixel in modo da farli rientrare nell'intervallo [0,1]
    data = np.array(data, dtype="float") / 255.0
    boxes = np.array(boxes)
    return (data, boxes)