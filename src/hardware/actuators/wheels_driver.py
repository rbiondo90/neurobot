from RPi import GPIO
import os
from utils.generic import defaults
from configparser import ConfigParser

__SETTINGS_FILE_PATH = os.path.join(defaults.CONFIG_DIRECTORY, (__name__.split(".")[-1] + ".ini"))


class MotorController(object):

    SPEED_LEVELS = 10
    _PWM_FREQUENCY = 1000
    _MIN_PWM = 40
    _MAX_PWM = 100

    def __init__(self, GPIO_set_1, GPIO_set_2, GPIO_speed_control):
        GPIO.setmode(GPIO.BCM)  # Setting GPIOs to BCM Mode (Pin number = GPIO number)
        self.__GPIO_set_1 = GPIO_set_1
        self.__GPIO_set_2 = GPIO_set_2
        self.__GPIO_speed_control = GPIO_speed_control
        # GPIO pins to output mode
        GPIO.setup(self.__GPIO_set_1, GPIO.OUT)
        GPIO.setup(self.__GPIO_set_2, GPIO.OUT)
        GPIO.setup(self.__GPIO_speed_control, GPIO.OUT)
        self.__PWM = GPIO.PWM(self.__GPIO_speed_control, self._PWM_FREQUENCY)
        self.__PWM.start(self._MIN_PWM)
        self.__speed_dutycycle_mapping = [0, self._MIN_PWM]
        pwm_step = (self._MAX_PWM - self._MIN_PWM) / float(self.SPEED_LEVELS - 1)
        for i in range(self.SPEED_LEVELS - 1):
            self.__speed_dutycycle_mapping.append(self.__speed_dutycycle_mapping[-1] + pwm_step)
        self.__speed_dutycycle_mapping = [int(level) for level in self.__speed_dutycycle_mapping]
        #self.__speed_dutycycle_mapping = [0, 40, 45, 50, 55, 60, 65, 70, 80, 90, 100]
        self.speed = 0

    @property
    def speed(self):
        return self.__speed

    @speed.setter
    def speed(self, speed):
        if abs(speed) in range(self.SPEED_LEVELS + 1):
            self.__speed = speed
            if speed != 0:
                if speed < 0:
                    speed = -speed
                    self.__set_pins(GPIO.LOW, GPIO.HIGH)
                else:
                    self.__set_pins(GPIO.HIGH, GPIO.LOW)
                self.__PWM.ChangeDutyCycle(self.__speed_dutycycle_mapping[abs(speed)])
            else:
                self.__set_pins(GPIO.LOW, GPIO.LOW)
        else:
            raise ValueError("Parametro errato per la velocita' del motore: inserire un valore tra 0 e 10.")

    def __set_pins(self, pin1_val, pin2_val):
        if pin1_val not in range(0, 2) or pin2_val not in range(0, 2):
            raise ValueError("Parametri di settaggio dei pin del motore errati: inserire un valore tra 0 e 1 per "
                             "ogni pin.")
        elif pin1_val == pin2_val == 1:
            raise ValueError("Combinazione di pin del motore non ammessa.")
        else:
            GPIO.output(self.__GPIO_set_1, GPIO.LOW)
            GPIO.output(self.__GPIO_set_1, GPIO.HIGH)
            GPIO.output(self.__GPIO_set_1, pin1_val)
            GPIO.output(self.__GPIO_set_2, pin2_val)

    def forward(self):
        if self.speed > 0:
            return
        elif self.speed < 0:
            self.speed = -1 * self.speed
        else:
            self.speed = 1

    def backwards(self):
        if self.speed < 0:
            return
        elif self.speed > 0:
            self.speed = -1 * self.speed
        else:
            self.speed = 1

    def stop(self):
        self.speed = 0


__config = ConfigParser()
__config.read(__SETTINGS_FILE_PATH)

left_wheel = MotorController(__config.getint("left_wheel", "GPIO_SET_1"), __config.getint("left_wheel", "GPIO_SET_2"),
                             __config.getint("left_wheel", "GPIO_speed_control"))

right_wheel = MotorController(__config.getint("right_wheel", "GPIO_SET_1"),
                              __config.getint("right_wheel", "GPIO_SET_2"),
                              __config.getint("right_wheel", "GPIO_speed_control"))
