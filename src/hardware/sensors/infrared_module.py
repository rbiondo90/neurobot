'''
 Il modulo infrarossi utilizza il pin OUT per mandare un semplice segnale binario:
 True se qualcosa è stato rilevato nel range di visibilità del sensore, False altrimenti.
 '''
import RPi.GPIO as GPIO
from time import sleep

class InfraredModule:
    def __init__(self, ir_pin):
        GPIO.setmode(GPIO.BCM)
        self.ir_pin = ir_pin
        GPIO.setup(self.ir_pin, GPIO.IN)

    def get_state(self):
        if GPIO.input(self.ir_pin):
            return True
        else:
            return False

    def ir_start(self, update_interval=0.2):
        while True:
            if self.get_state():
                # what to do when obstacle in range
                print("Obstacle in range!")
                sleep(update_interval)
