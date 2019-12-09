#!/usr/bin/python
# -*- coding: utf-8 -*-

# https://www.waveshare.com/wiki/High-Precision_AD/DA_Board


import RPi.GPIO as GPIO          #calling header file which helps us use GPIO’s of PI
import time                    #calling time to provide delays in program
import sys
import os
from ADS1256_definitions import *
from pipyadc import ADS1256

if not os.path.exists("/dev/spidev0.1"):
        raise IOError("Error: No SPI device. Check settings in /boot/config.txt")
    
pin_sensor1 = 37
GPIO.setwarnings(False)  # do not show any warnings
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin_sensor1, GPIO.OUT)


print("Here1")

EXT2, EXT3, EXT4 = POS_AIN2 | NEG_AINCOM, POS_AIN3 | NEG_AINCOM, POS_AIN4 | NEG_AINCOM
EXT5, EXT6, EXT7 = POS_AIN5 | NEG_AINCOM, POS_AIN6 | NEG_AINCOM, POS_AIN7 | NEG_AINCOM

CH_SEQUENCE = (EXT2, EXT3, EXT4, EXT7)

class Wheel:
    def read_sensor(self, sensor_location):
        raw_channels = ads.read_sequence(sensor_location)
        voltages = [i * ads.v_per_digit for i in raw_channels]
        print(voltages)
        return voltages

    def control_valve(self, PWM, dutyratio):
        PWM.ChangeDutyCycle(dutyratio)             # change duty cycle for varying the brightness of LED.

    def control_pump(self, PWM, dutyratio):
        PWM.ChangeDutyCycle(dutyratio)             # change duty cycle for varying the brightness of LED.
        print("pump")

print("Here2")
ads = ADS1256()
ads.cal_self()
wheels = Wheel()

p = GPIO.PWM(pin_sensor1, 50)          # GPIO as PWM output, with 100Hz frequency
p.start(0)

while True:
    volts = wheels.read_sensor(CH_SEQUENCE)
    if -1 <= volts[1] < 0.5:
        wheels.control_pump(p, 100)
        print("One")
    elif 0.5 <= volts[1] < 1:
        wheels.control_pump(p, 66)
        print("Two")
    elif 1 <= volts[1] < 2:
        wheels.control_pump(p, 33)
        print("Three")
    elif 2 <= volts[1]:
        wheels.control_pump(p, 0)
        print("Four")


def set_contants():
    upper_threshold = 3.4
    lower_threshold = 3.6


def set_pins():  # sets all of the pins based off the config
    pin_sensor1 = 37
    GPIO.setwarnings(False)  # do not show any warnings
    GPIO.setmode(GPIO.BOARD)  # we are programming the GPIO by BCM pin numbers. (PIN35 as ‘GPIO19’)
    GPIO.setup(pin_sensor1, GPIO.OUT)  # initialize GPIO19 as an output.

    EXT2, EXT3, EXT4 = POS_AIN2 | NEG_AINCOM, POS_AIN3 | NEG_AINCOM, POS_AIN4 | NEG_AINCOM
    EXT5, EXT6, EXT7 = POS_AIN5 | NEG_AINCOM, POS_AIN6 | NEG_AINCOM, POS_AIN7 | NEG_AINCOM

    CH_SEQUENCE = (EXT2, EXT3, EXT4, EXT7)
