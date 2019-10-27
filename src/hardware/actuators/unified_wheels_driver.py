from wheels_driver import MotorController, left_wheel, right_wheel


class __UnifiedWheelsDriver(object):

    left_wheel = left_wheel
    right_wheel = right_wheel

    def __init__(self):
        self.__speed = 0
        self.__direction = 0

    def __update_wheels_speed(self):
        self.__speed = left_wheel.speed, right_wheel.speed

    def __normalize_direction(self, direction):
        return float(direction)/10. + 0.5

    @property
    def direction(self):
        pass

    @property
    def speed(self):
        return self.__speed

    @speed.setter
    def speed(self, speed):
        self.__speed = speed
        self.__update_wheels_speed()

    def stop(self):
        self.speed = 0


driver = __UnifiedWheelsDriver()
