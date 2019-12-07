from gpiozero import DistanceSensor
from time import sleep

# gpiozero doc: https://gpiozero.readthedocs.io/en/stable/api_input.html#gpiozero.DistanceSensor
# source code: https://gpiozero.readthedocs.io/en/stable/_modules/gpiozero/input_devices.html#DistanceSensor


class UltrasonicModule:
    def __init__(self, gpio_echo, gpio_trigger):
        # class gpiozero.DistanceSensor(echo, trigger, *,
        # queue_len=30, max_distance=1, threshold_distance=0.3, partial=False, pin_factory=None)
        self.sensor = DistanceSensor(echo=gpio_echo, trigger=gpio_trigger, threshold_distance=0.99)

    def set_threshold_distance(self, new_threshold_distance):
        if abs(new_threshold_distance) >= 1:
            print("Value out of range! Try again with a value 0 < x < 1")
        else:
            self.sensor.threshold_distance = new_threshold_distance

    # def obstacle_in_range(self):
    #     print("Obstacle in range!")
    #
    # def obstacle_out_range(self):
    #     print("Obstacle out of range")
    #
    #
    # def smart_start(self):
    #     while True:
    #         self.sensor.when_in_range = self.obstacle_in_range
    #         self.sensor.when_out_of_range = self.obstacle_out_range

    def smart_start(self, update_interval=0.2):
        while True:
            if self.sensor.in_range:
                print("Obstacle in %.4f cm" % self.sensor.distance)
            else:
                print("No obstacles in range")
            sleep(update_interval)
