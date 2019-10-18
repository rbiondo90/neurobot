"""
* Partiamo dall'immagine rgb, la convertiamo in HSV, usiamo la funzione inrange che esegue il treshold dell'immagine
  a partire da un range di colori. Funzione: inRange(lower, upper)
* Otterremo una immagine binaria che rappresenta la maschera
* Sulla maschera otteniamo il bounding box
* Calcoliamo l'area
* Misuriamo la distanza
"""
from esercizi_opencv.camera import CameraImage
import cv2
import json


class DistanceComputer:
    default_setting_file_path = 'esercizi_opencv/distanza_oggetto.json'

    def __init__(self, path_to_settings=default_setting_file_path):
        self.camera = CameraImage()
        with open(path_to_settings, 'r') as settings_file:
            settings = json.load(settings_file)
        self.lower_bound = tuple(settings["colorParameters"]["lowerBound"])
        self.upper_bound = tuple(settings["colorParameters"]["upperBound"])
        self.mask_size = settings["gaussianBlurParameters"]["maskSize"]
        self.sigma = settings["gaussianBlurParameters"]["sigmaX"]
        self.erode_iterations = settings["erodeIterations"]
        self.dilate_iterations = settings["dilateIterations"]

    def get_filtered_image(self, image = None):
        if image is None:
            self.camera.setup()
            image = self.camera.get_image()
            self.camera.release()
        filtered = cv2.GaussianBlur(image, (self.mask_size, self.mask_size), self.sigma)
        lower_bound = (20, 125, 0)
        upper_bound = (40, 255, 255)
        hsv = cv2.cvtColor(filtered, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_bound, upper_bound)
        mask = cv2.erode(mask, None, iterations=3)
        mask = cv2.dilate(mask, None, iterations=3)
        return mask


if __name__ == '__main__':
    distanceComputer = DistanceComputer()
    cv2.imshow('', distanceComputer.get_filtered_image())
    while cv2.waitKey(1) & 0xFF != ord('q'):
        pass
    cv2.destroyWindow('')
