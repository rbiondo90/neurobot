import os
import sys
import time
os.chdir("/home/pi/project/neurobot")
sys.path.extend(["/home/pi/project/neurobot","/home/pi/project/neurobot/src"])

from recognizers.distance_interpolator import DistanceInterpolator
from recognizers.classic_d_bbr import ClassicObjectBBDetector
from utils.interactive_parameter_selector import InteractiveParameterSelector
from hardware.actuators.unified_wheels_driver import driver
from goal_logic.genetic_persecutor.genetic_persecutor import GeneticPersecutor
from hardware.sensors.pi_camera import PiCameraWrapper
from watcher.watcher import Watcher
from goal_logic.dumb_goer import Goer
import threading

camera = PiCameraWrapper(resolution=(256,256))
watcher = Watcher(camera=camera, distance_calculator=DistanceInterpolator("wheel.json"),
                  object_recognizer=ClassicObjectBBDetector("wheel.ini"))
selector = InteractiveParameterSelector(distance_interpolator_settings_file="wheel.json", camera=camera,
                                        detector_settings_file="wheel.ini")
goer = Goer(watcher, driver)

gp = GeneticPersecutor("first_try", watcher=watcher)
i = gp.current_generation.individuals[0]
s = threading.Thread(target=selector.start)

driver.speed = 5
time.sleep(0.2)
driver.speed = 0
time.sleep(0.2)
driver.speed = -5
time.sleep(0.2)
driver.speed = 0
