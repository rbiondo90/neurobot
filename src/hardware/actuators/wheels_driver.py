from RPi import GPIO
import os
import defaults
from configparser import ConfigParser

__SETTINGS_FILE_PATH = os.path.join(defaults.CONFIG_DIRECTORY, (__name__.split(".")[-1] + ".ini"))

class __MotorController:

    def __init__(self, GPIO_set_1, GPIO_set_2, GPIO_speed_control):
        GPIO.setmode(GPIO.BCM)      # Setting GPIOs to BCM Mode (Pin number = GPIO number)
        self.__GPIO_set_1 = GPIO_set_1
        self.__GPIO_set_2 = GPIO_set_2
        self.__GPIO_speed_control = GPIO_speed_control
        # GPIO pins to output mode
        GPIO.setup(self.__GPIO_set_1, GPIO.OUT)
        GPIO.setup(self.__GPIO_set_2, GPIO.OUT)
        GPIO.setup(self.__GPIO_speed_control, GPIO.OUT)
        self.__PWM = GPIO.PWM(self.__GPIO_speed_control, 1000)
        self.__PWM.start(15)
        self.__speed_dutycycle_mapping = [0, 25, 30, 35, 45, 50, 60, 70, 80, 90, 100]
        self.__speed = 1


    def set_speed(self, speed):
        self.__speed = speed
        if speed == 0:
            self.stop()
        elif speed in range(1,11):
            self.__PWM.ChangeDutyCycle(self.__speed_dutycycle_mapping[speed])
        else:
            print("Parametro errato per la velocita' del motore: inserire un valore tra 0 e 10.")

    def get_speed(self):
        return self.__speed

    def __set_pins(self, pin1_val, pin2_val):
        if pin1_val not in range(0,2) or pin2_val not in range(0,2):
            print("Parametri di settaggio dei pin del motore errati: inserire un valore tra 0 e 1 per ogni pin.")
        elif pin1_val == pin2_val == 1:
            print("Combinazione di pin del motore non ammessa.")
        else:
            GPIO.output(self.__GPIO_set_1, GPIO.LOW)
            GPIO.output(self.__GPIO_set_1, GPIO.HIGH)
            GPIO.output(self.__GPIO_set_1, pin1_val)
            GPIO.output(self.__GPIO_set_2, pin2_val)

    def forward(self):
        if self.__speed == 0:
            self.set_speed(1)
        self.__set_pins(GPIO.HIGH, GPIO.LOW)

    def backwards(self):
        if self.__speed == 0:
            self.set_speed(1)
        self.__set_pins(GPIO.LOW, GPIO.HIGH)

    def stop(self):
        self.__set_pins(GPIO.LOW, GPIO.LOW)

__config = ConfigParser()
__config.read(__SETTINGS_FILE_PATH)

left_wheel = __MotorController(__config.getint("left_wheel","GPIO_SET_1"), __config.getint("left_wheel","GPIO_SET_2"),
                               __config.getint("left_wheel","GPIO_speed_control"))

right_wheel = __MotorController(__config.getint("right_wheel","GPIO_SET_1"), __config.getint("right_wheel","GPIO_SET_2"),
                               __config.getint("right_wheel","GPIO_speed_control"))

