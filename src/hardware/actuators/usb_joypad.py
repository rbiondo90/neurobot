from inputs import devices
from utils.generic.daemon import Daemon


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
