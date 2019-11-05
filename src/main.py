import os
import sys
import time
import atexit

os.chdir("/home/pi/project/neurobot")
sys.path.extend(["/home/pi/project/neurobot", "/home/pi/project/neurobot/src"])

from recognizers.distance_interpolator import DistanceInterpolator
from recognizers.classic_d_bbr import ClassicObjectBBDetector
from utils.interactive_parameter_selector import InteractiveParameterSelector
from hardware.actuators.unified_wheels_driver import driver
from goal_logic.genetic_persecutor.genetic_persecutor import GeneticPersecutor
from hardware.sensors.pi_camera import PiCameraWrapper
from watcher.watcher import Watcher
from goal_logic.dumb_goer import Goer
from utils.web_logger.web_server import WebLogger
from utils.human_control import HumanControl
from utils.daemon import Daemon


def exit_handler():
    if camera is not None and camera.dev is not None:
        camera.release()


atexit.register(exit_handler)
camera = PiCameraWrapper(resolution=(128, 128))
watcher = Watcher(camera=camera, distance_calculator=DistanceInterpolator("estintore.json"),
                  object_recognizer=ClassicObjectBBDetector("estintore.ini"))
selector = InteractiveParameterSelector(distance_interpolator_settings_file="estintore.json", camera=camera,
                                        detector_settings_file="estintore.ini")
goer = Goer(watcher, driver)

# gp = GeneticPersecutor("first_try", watcher=watcher)
# i = gp.current_generation.individuals[0]
# ws = WebLogger(watcher=watcher, wheels_driver=driver)
s = Daemon(target=selector.start)
try:
    hc = HumanControl()
except:
    pass
# ws.run()

driver.speed = 5
time.sleep(0.2)
driver.speed = 0
time.sleep(0.2)
driver.speed = -5
time.sleep(0.2)
driver.speed = 0
