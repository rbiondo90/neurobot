from hardware.actuators.joypads import USBJoypad, PS4Joypad
from hardware.actuators.unified_wheels_driver import driver
import time
from utils.generic.daemon import Daemon


class HumanControl:

    def __init__(self):
        self.daemon = None
        self.joy = None
        self.enabled = False
        self.paused = False
        self.start()

    def _control_loop(self):
        self._wait_for_joypad()
        self._handle_inputs()

    def _wait_for_joypad(self, first=False):
        first = True
        while True:
            try:
                self.joy = PS4Joypad()
                self.joy.enable()
                print("[HumanControl] Joypad collegato. Premere options per attivare/disattivare il controllo "
                      "manuale del robot.")
                break
            except RuntimeError:
                if first:
                    print("[HumanControl] Non riesco a connettermi al Joypad. Controllare che sia attivo "
                          "ed accoppiato al robot.")
                first = False
                time.sleep(0.5)

    def start(self):
        if not self.enabled:
            self.enabled = True
            self.daemon = Daemon(target=self._control_loop)
            self.daemon.start()
            print("[HumanControl] Inizializzato.")
        else:
            print("[HumanControl] Gia' avviato.")

    def _handle_inputs(self):
        while self.enabled:
            if self.joy.options.pressed:
                self.paused = not self.paused
                print("[HumanControl] " + (" In pausa " if self.paused else " Nuovamente attivo."))
            if not self.paused:
                x = self.joy.left_analog[0]
                y = self.joy.left_analog[1]
                if y not in range(118, 139):
                    speed = int(10 - y / 12.75)
                    direction = int(x / 42.5 - 3)
                else:
                    speed = int(abs(10 - x / 12.75))
                    direction = -driver.DIRECTION_LEVELS if x < 128 else driver.DIRECTION_LEVELS
                driver.speed = speed
                driver.direction = direction
            time.sleep(0.1)

    def stop(self):
        if self.enabled:
            self.enabled = False
            self.joy.disable()
            driver.stop()
            print("[HumanControl] Arrestato.")
        else:
            print("[HumanControl] Non attivo.")
