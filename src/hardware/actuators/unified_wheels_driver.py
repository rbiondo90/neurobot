from wheels_driver import MotorController, left_wheel, right_wheel


class __UnifiedWheelsDriver(object):

    left_wheel = left_wheel
    right_wheel = right_wheel

    def __init__(self):
        self.__speed = 0
        self.__direction = 0.
        self.__update_wheels_speed()

    def __update_wheels_speed(self):
        self.right_wheel.speed = int(min(round((1. - self.__direction) * self.__speed), 10.))
        self.left_wheel.speed = int(min((round(1. + self.__direction) * self.__speed), 10.))

    def __normalize_direction(self, direction):
        return float(direction)/10. + 0.5

    @property
    def direction(self):
        return int(self.__direction * 10)

    @direction.setter
    def direction(self, direction):
        if direction in range(-10,11):
            self.__direction = float(direction) / 10.
            self.__update_wheels_speed()
        else:
            raise ValueError("Specificare una direzione nell'intervallo [-10,10]")

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
