from inputs import devices
from utils.generic.daemon import Daemon
from evdev import InputDevice, categorize, ecodes
import glob

class USBJoypad:

    def __init__(self, idx=0):
        self.dev = devices.gamepads[idx]
        self.left_analog = [128, 128]
        self.enable()

    def test(self):
        while 1:
            events = self.dev.read()
            for event in events:
                print(event.ev_type, event.code, event.state)

    def enable(self):
        self.enabled = True

        def status_refresh():
            while self.enabled:
                events = self.dev.read()
                found = 0
                for event in events:
                    if event.code == "ABS_X":
                        self.left_analog[0] = event.state
                        found += 1
                    elif event.code == "ABS_Y":
                        self.left_analog[1] = event.state
                        found += 1
                    if found == 2:
                        break

        Daemon(target=status_refresh).start()

    def disable(self):
        self.enabled = False

class PS4Joypad:
    LEFT_ANALOG_X_EV_CODE = 0
    LEFT_ANALOG_Y_EV_CODE = 1

    def __init__(self):
        for elem in glob.glob("/dev/input/event*"):
            if InputDevice(elem).name == "Wireless Controller":
                self.dev = InputDevice(elem)
        if self.dev is None:
            raise RuntimeError("Non trovo il controller PS4")
        self.left_analog = [128, 128]
        #self.enable()

    def test(self):
        for event in self.dev.read_loop():
            if event.code == self.LEFT_ANALOG_Y_EV_CODE and event.value > 0:
                print(event.code, event.value, event.type)

    def enable(self):
        self.enabled = True

        def status_refresh():
            for event in self.dev.read_loop():
                if self.enabled:
                    if event.type == 3 and event.code == self.LEFT_ANALOG_X_EV_CODE:
                        self.left_analog[0] = event.value
                    elif event.type == 3 and event.code == self.LEFT_ANALOG_Y_EV_CODE:
                         self.left_analog[1] = event.value
                else:
                    break

        Daemon(target=status_refresh).start()

    def disable(self):
        self.enabled = False
