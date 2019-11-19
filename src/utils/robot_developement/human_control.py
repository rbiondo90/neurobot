from hardware.actuators.joypads import USBJoypad, PS4Joypad
from hardware.actuators.unified_wheels_driver import driver
import time
from utils.generic.daemon import Daemon


class HumanControl:

    def __init__(self):
        try:
            self.joy = PS4Joypad()
        except RuntimeError:
            self.joy = USBJoypad()
        self.enabled = False

    def start(self):
        self.enabled = True
        self.joy.enable()

        def thread_func():
            while self.enabled:
                x = self.joy.left_analog[0]
                y = self.joy.left_analog[1]
                if y not in range(118, 139):
                    speed = int(10 - y / 12.75)
                    direction = int(x / 42.5 - 3)
                else:
                    speed = int(abs(10 - x / 12.75))
                    direction = -3 if x < 128 else 3
                driver.speed = speed
                driver.direction = direction
                time.sleep(0.1)

        Daemon(target=thread_func).start()

    def stop(self):
        self.enabled = False
        self.joy.disable()
