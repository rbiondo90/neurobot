"""
Classic detector and boundary box recognizer
"""
import cv2
import os
from utils import defaults
from configparser import ConfigParser
import shutil
import numpy as np

class ClassicObjectBBDetector:
    SETTINGS_FILES_PATH = os.path.join(defaults.CONFIG_DIRECTORY, __name__.split(".")[-1])
    DEFAULT_SETTINGS_FILE_PATH = os.path.join(SETTINGS_FILES_PATH, "defaults.ini")
    SETTINGS_FILE_PATH = os.path.join(SETTINGS_FILES_PATH, "settings.ini")

    def __init__(self, custom_settings_file=None):
        if custom_settings_file is None:
            self.specific_settings_file_path = self.SETTINGS_FILE_PATH
        else:
            self.specific_settings_file_path = os.path.join(self.SETTINGS_FILES_PATH, custom_settings_file)
        self.reload_settings()
        self.filter_contours = True

    def reload_settings(self):
        # Se il file non esiste ancora, viene copiato ed utilizzato il file delle impostazioni di default
        if not os.path.isfile(self.specific_settings_file_path):
            shutil.copyfile(self.DEFAULT_SETTINGS_FILE_PATH, self.specific_settings_file_path)
        config = ConfigParser()
        config.read(self.specific_settings_file_path)
        self.lower_bound = [int(x) for x in config["color_parameters"]["lower_bound"].split(" ")]
        self.upper_bound = [int(x) for x in config["color_parameters"]["upper_bound"].split(" ")]
        self.mask_size = config.getint("gaussian_blur_parameters","mask_size")
        self.sigma = config.getint("gaussian_blur_parameters","sigma_x")
        self.erode_iterations = config.getint("other","erode_iterations")
        self.dilate_iterations = config.getint("other","dilate_iterations")

    def save_settings(self):
        config = ConfigParser()
        config.add_section("color_parameters")
        config["color_parameters"]["lower_bound"] = " ".join(str(x) for x in self.lower_bound)
        config["color_parameters"]["upper_bound"] = " ".join(str(x) for x in self.upper_bound)
        config.add_section("gaussian_blur_parameters")
        config["gaussian_blur_parameters"]["mask_size"] = str(self.mask_size)
        config["gaussian_blur_parameters"]["sigma_x"] = str(self.sigma)
        config.add_section("other")
        config["other"]["erode_iterations"] = str(self.erode_iterations)
        config["other"]["dilate_iterations"] = str(self.dilate_iterations)
        with open(self.specific_settings_file_path, 'w') as config_file:
            config.write(config_file)

    def get_image_mask(self, image):
        filtered_image = cv2.GaussianBlur(image, (self.mask_size, self.mask_size), self.sigma)
        hsv = cv2.cvtColor(filtered_image, cv2.COLOR_BGR2HSV)
        #hsv[:,:,2] = cv2.equalizeHist(hsv[:,:,2])
        mask = cv2.inRange(hsv, tuple(self.lower_bound), tuple(self.upper_bound))
        mask = cv2.erode(mask, None, iterations=self.erode_iterations)
        mask = cv2.dilate(mask, None, iterations=self.dilate_iterations)
        return mask

    def get_object_boundary_box(self, mask):
        contours = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[0]
        if len(contours) > 0:
            contour = max(contours, key=cv2.contourArea)
            return cv2.boundingRect(contour)
        return None

    def get_area(self, boundary_box):
        if boundary_box is not None:
            return boundary_box[2]*boundary_box[3]
        return None

    def recognize_object(self, image):
        mask = self.get_image_mask(image)
        boundary_box = self.get_object_boundary_box(mask)
        if boundary_box is not None:
            area = self.get_area(boundary_box)
            horizontal_position = self.get_horizontal_position(image.shape[1], boundary_box)
            return True, boundary_box, area, horizontal_position
        return False, None, None, None

    def get_horizontal_position(self, image_width, boundary_box):
        if boundary_box is not None:
            norm_horizontal_center = (float((boundary_box[0] + boundary_box[2]))/image_width)*2. - 1.
            return norm_horizontal_center
        return None

if __name__ == '__main__':
    distanceComputer = ClassicObjectBBDetector()
    im = cv2.imread('giallo.jpg')
    cv2.imshow('', distanceComputer.get_image_mask(im))
    while cv2.waitKey(1) & 0xFF != ord('q'):
        pass
    cv2.destroyWindow('')
