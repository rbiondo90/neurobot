from hardware.actuators.usb_joypad import USBJoypad
from hardware.actuators.unified_wheels_driver import driver
import time
from utils.daemon import Daemon


class HumanControl:

    def __init__(self):
        self.joy = USBJoypad()
        self.enabled = False

    def start(self):
        self.enabled = True
        self.joy.enable()

        def thread_func():
            while self.enabled:
                x = self.joy.left_analog[0]
                y = self.joy.left_analog[1]
                speed = int(10 - y / 12.75)
                direction = int(x / 63. - 2)
                if speed == 0 and direction != 0:
                    speed = int(abs(10 - x / 12.75))
                    direction = -3 if direction < 0 else 3
                driver.speed = speed
                driver.direction = direction
                time.sleep(0.1)

        Daemon(target=thread_func).start()

    def stop(self):
        self.enabled = False
        self.joy.disable()
