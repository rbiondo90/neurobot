from gpiozero import DistanceSensor
from time import sleep
from signal import pause

# gpiozero doc: https://gpiozero.readthedocs.io/en/stable/api_input.html#gpiozero.DistanceSensor
# source code: https://gpiozero.readthedocs.io/en/stable/_modules/gpiozero/input_devices.html#DistanceSensor


GPIO_TRIGGER = 0    # Map to Pi
GPIO_ECHO = 0       # Map to Pi

class UltrasonicModule:
    def __init__(self):
        # class gpiozero.DistanceSensor(echo, trigger, *,
        # queue_len=30, max_distance=1, threshold_distance=0.3, partial=False, pin_factory=None)
        self.sensor = DistanceSensor(echo=GPIO_ECHO, trigger=GPIO_TRIGGER)

    def is_obstacle_present(self):
        if self.sensor.in_range():
            return True
        else:
            return False



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
    #         pause()

    def smart_start(self):
        while True:
            if self.is_obstacle_present():
                print(f"Obstacle in {self.sensor.distance() / 100 } cm")
            else:
                print("No obstacles in range")
