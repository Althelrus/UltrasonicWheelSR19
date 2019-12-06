#!/usr/bin/python
# -*- coding: utf-8 -*-

# https://www.waveshare.com/wiki/High-Precision_AD/DA_Board


import RPi.GPIO as IO          #calling header file which helps us use GPIO’s of PI
import time                    #calling time to provide delays in program
import sys
import os
from ADS1256_definitions import *
from pipyadc import ADS1256

IO.setwarnings(False)  # do not show any warnings
IO.setmode(IO.BCM)  # we are programming the GPIO by BCM pin numbers. (PIN35 as ‘GPIO19’)
IO.setup(37, IO.OUT)  # initialize GPIO19 as an output.
pin_sensor1 = 37

EXT2, EXT3, EXT4 = POS_AIN2 | NEG_AINCOM, POS_AIN3 | NEG_AINCOM, POS_AIN4 | NEG_AINCOM
EXT5, EXT6, EXT7 = POS_AIN5 | NEG_AINCOM, POS_AIN6 | NEG_AINCOM, POS_AIN7 | NEG_AINCOM

CH_SEQUENCE = (EXT2, EXT3, EXT4, EXT7)

class Wheel:
    def read_sensor(self, sensor_location):
        raw_channels = ads.read_sequence(sensor_location)
        voltages = [i * ads.v_per_digit for i in raw_channels]
        print(voltages)
        return voltages

    def control_valve(self, valve_location, freq, dutyratio):
        p = IO.PWM(valve_location, freq)         # GPIO as PWM output, with 100Hz frequency
        p.ChangeDutyCycle(dutyratio)             # change duty cycle for varying the brightness of LED.

    def control_pump(self, pump_location, freq, dutyratio):
        p = IO.PWM(pump_location, freq)          # GPIO as PWM output, with 100Hz frequency
        p.ChangeDutyCycle(dutyratio)             # change duty cycle for varying the brightness of LED.


def set_contants():
    upper_threshold = 3.4
    lower_threshold = 3.6


def set_pins():  # sets all of the pins based off the config
    IO.setwarnings(False)  # do not show any warnings
    IO.setmode(IO.BCM)  # we are programming the GPIO by BCM pin numbers. (PIN35 as ‘GPIO19’)
    IO.setup(37, IO.OUT)  # initialize GPIO19 as an output.
    pin_sensor1 = 37

    EXT2, EXT3, EXT4 = POS_AIN2 | NEG_AINCOM, POS_AIN3 | NEG_AINCOM, POS_AIN4 | NEG_AINCOM
    EXT5, EXT6, EXT7 = POS_AIN5 | NEG_AINCOM, POS_AIN6 | NEG_AINCOM, POS_AIN7 | NEG_AINCOM

    CH_SEQUENCE = (EXT2, EXT3, EXT4, EXT7)


if __name__ == "main":
    
    if not os.path.exists("/dev/spidev0.1"):
        raise IOError("Error: No SPI device. Check settings in /boot/config.txt")
        # special_print()  # Print to web server Error

    # set_contants()  # Set default constants for first time boot
    # set_pins()  # Set Pins
    ads = ADS1256()
    ads.cal_self()

    wheels = Wheel()

    while True:
        volts = wheels.read_sensor(pin_sensor1)
        print(volts)
        if 0 <= volts[1] < 1:
            wheels.control_pump(EXT3, 50, 100)
            print("One")
        elif 1 <= volts[1] < 2:
            wheels.control_pump(EXT3, 50, 66)
            print("Two")
        elif 2 <= volts[1] < 3:
            wheels.control_pump(EXT3, 50, 33)
            print("Three")
        elif 3 <= volts[1]:
            wheels.control_pump(EXT3, 50, 0)
            print("Four")







