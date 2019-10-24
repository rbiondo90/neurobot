from hardware.camera import Camera
# from recognizers.object_recognizer.object_recognizer_net import ObjectRecognizerNet
# from recognizers.object_bounding_box_recognizer.object_bounding_box_recognizer import ObjectBoundingBoxRecognizer
from recognizers.classic_d_bbr import ClassicObjectBBDetector
import cv2
import numpy as np
from utils import util


class Watcher:

    def __init__(self, object_recognizer=None):
        if object_recognizer is None:
            object_recognizer = ClassicObjectBBDetector()
        #     object_recognizer = ObjectRecognizerNet().contains_object
        # if object_bounding_box_recognizer is None:
        #     object_bounding_box_recognizer = ObjectBoundingBoxRecognizer().predict

        self.camera = Camera()
        self.object_recognizer = object_recognizer
        # self.object_bounding_box_recognizer = object_bounding_box_recognizer

    def get_bounding_box_area(self, bounding_box):
        return (bounding_box[1] - bounding_box[0]) * (bounding_box[3] - bounding_box[2])

    def get_distance(self, area):
        return area

    def elaborate_image(self, image):
        # found_object, probability = self.object_recognizer.contains_object(image)
        image_copy = np.copy(image)
        found_object, object_bounding_box, object_distance, object_position = self.object_recognizer.recognize_object(image)
        text = "object %s detected" % ("" if found_object else "not")
        if found_object:
            # # de_normalization_x = image_copy.shape[1]/128.
            # # de_normalization_y = image_copy.shape[0]/128.
            # bounding_box_coords = self.object_bounding_box_recognizer.predict(image)
            area = self.get_bounding_box_area(object_bounding_box)
            # # bounding_box_coords[0:2] *= de_normalization_x
            # # bounding_box_coords[2:4] *= de_normalization_y
            # bounding_box_coords[0:2] *= image_copy.shape[1]
            # bounding_box_coords[2:4] *= image_copy.shape[0]
            # bounding_box_coords = bounding_box_coords.astype(int)
            # if (bounding_box_coords[1] - bounding_box_coords[0]) < 0 or (bounding_box_coords[3] - bounding_box_coords[2]) <0:
            #     print("Wrong coords")
            # else:
            cv2.rectangle(image_copy, (object_bounding_box[0], object_bounding_box[2]),
                          (object_bounding_box[1],object_bounding_box[3]),(255,255,255))
            cv2.putText(image_copy, "Bounding box area: %d" % int(area), (5, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, 2)
        cv2.putText(image_copy, text, (5, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, 2)
        if image_copy.shape[0] < 640 or image_copy.shape[1] < 480:
            image_copy = cv2.resize(image_copy, (640, 480))
        return image_copy

    def watch(self):
        self.camera.show_video('Watcher camera video output', frame_elaboration_function=self.elaborate_image, frame_interval=10)

    def watch_image(self, image):
        if type(image) == str:
            image = cv2.imread(image)
        util.imshow('Watcher image output', self.elaborate_image(image))


if __name__ == '__main__':
    watcher = Watcher()
    print("Watcher inizializzato")
    image = cv2.imread('data/datasets/item_no_item_dataset/item/20191014_155049_024.jpg')
    image = cv2.resize(image, (640,640))
    watcher.watch_image(image)
