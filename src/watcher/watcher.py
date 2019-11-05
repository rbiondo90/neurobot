from hardware.sensors.pi_camera import PiCameraWrapper
from recognizers.classic_d_bbr import ClassicObjectBBDetector
from recognizers.distance_interpolator import DistanceInterpolator
import numpy as np

class Watcher:

    def __init__(self, object_recognizer=None, distance_calculator=None, camera=None):
        if object_recognizer is None:
            object_recognizer = ClassicObjectBBDetector()
        if distance_calculator is None:
            distance_calculator = DistanceInterpolator("wheel.json")
        if camera is None:
            camera = PiCameraWrapper
        self.camera = camera
        self.object_recognizer = object_recognizer
        self.distance_calculator = distance_calculator

    def get_distance(self, area):
        return self.distance_calculator.get_distance(area) if area is not None else None

    def watch(self, image=None):
        if image is None:
            image = self.camera.get_image()
        recognized, bounding_rectangle, area, horizontal_position = self.object_recognizer.recognize_object(image)
        return recognized, self.get_distance(area), horizontal_position

