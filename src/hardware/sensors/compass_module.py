# Doc: https://pypi.org/project/mpu6050-raspberrypi/
# Installation:
# 1 - sudo apt install python3-smbus
# 2 - pip install mpu6050-raspberrypi

from mpu6050 import mpu6050
from time import sleep

# Connection doc: http://blog.bitify.co.uk/2013/11/interfacing-raspberry-pi-and-mpu-6050.html
'''
To connect the sensor you need to use the GPIO pins on the Pi, the important pins are
Pin 1 - 3.3V connect to VCC
Pin 3 - SDA connect to SDA
Pin 5 - SCL connect to SCL
Pin 6 - Ground connect to GND
these need to be connect as shown in the image.

Once you have the board connected you can test to see if the Pi has detected it.  This is done with the following
command to install the i2c tools

sudo apt-get install i2c-tools
and then either
sudo i2cdetect -y 0 (for a Revision 1 board like mine)
or
sudo i2cdetect -y 1 (for a Revision 2 board)

then you should see output showing any I2C devices that are attached and their addresses

This shows that the Pi has detected the sensor with an address of 0x68 (hexadecimal), this address is needed to interact with it.
Enter the following command and you should get an output of 0x68 on screen if everything is working properly.
sudo i2cget -y 0 0x68 0x75
'''

class CompassModule:
    def __init__(self, address=0x68):
        self.sensor = mpu6050(address)

    def get_data(self):
        accelerometer_data = self.sensor.get_accel_data()
        print(accelerometer_data)