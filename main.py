#!/usr/bin/python
# -*- coding: utf-8 -*-

# https://www.waveshare.com/wiki/High-Precision_AD/DA_Board


import RPi.GPIO as IO          #calling header file which helps us use GPIO’s of PI
import time                    #calling time to provide delays in program
import sys
import os
from ADS1256_definitions import *
from pipyadc import ADS1256


class Wheel:
    def wheel(self):
        valves = {}     # Holds the pin location to control the valves objects
        sensors = {}    # Holds the pin locations for the sensors objects
        pump = {}       # Holds the two pumps objects these objects are made up of direction and pin value
    
    def read_sensor(sensor_location):
        raw_channels = ads.read_sequence(CH_SEQUENCE)
        voltages = [i * ads.v_per_digit for i in raw_channels]

    def control_valve(valve_location, freq, dutyratio):
        p = IO.PWM(valve_location, freq)         # GPIO as PWM output, with 100Hz frequency
        p.start(0)                               # generate PWM signal with 0% duty cycle
        p.ChangeDutyCycle(dutyratio)             # change duty cycle for varying the brightness of LED.

    def control_pump(pump_location, freq, dutyratio):
        p = IO.PWM(pump_location, freq)          # GPIO as PWM output, with 100Hz frequency
        p.start(0)                               # generate PWM signal with 0% duty cycle
        p.ChangeDutyCycle(dutyratio)             # change duty cycle for varying the brightness of LED.
    
    
class GUI():
    def GUI(self):
        pass
    
    def run_web_Ui(self): # make threadable
        pass

    
if __name__ == "main": # make threadable
    
    if not os.path.exists("/dev/spidev0.1"):
        raise IOError("Error: No SPI device. Check settings in /boot/config.txt")
        # special_print()  # Print to web server Error
        
    ads = ADS1256()
    ads.cal_self()
    
    try:
        reload_config()  # Load Config
    except:
        set_contants()   # Set default contants for first time boot
        make_config()    # make config if not there
        
    set_pins()      # Set Pins
    GUI()           # Init web UI


def set_contants():
    upper_threshold = 3.4
    lower_threshold = 3.6


def set_pins():             # sets all of the pins based off the config
    IO.setwarnings(False)       # do not show any warnings
    IO.setmode (IO.BCM)         # we are programming the GPIO by BCM pin numbers. (PIN35 as ‘GPIO19’)
    IO.setup(19,IO.OUT)         # initialize GPIO19 as an output.
    # ==> Each channel in this context represents a differential pair of physical
    # input pins of the ADS1256 input multiplexer.
    #
    # ==> For single-ended measurements, simply select AINCOM as the negative input.
    #
    # AINCOM does not have to be connected to AGND (0V), but it is if the jumper
    # on the Waveshare board is set.
    #
    # Input pin for the potentiometer on the Waveshare Precision ADC board:
    # POTI = POS_AIN0|NEG_AINCOM
    # Light dependant resistor of the same board:
    # LDR  = POS_AIN1|NEG_AINCOM
    # The other external input screw terminals of the Waveshare board:
    EXT2, EXT3, EXT4 = POS_AIN2|NEG_AINCOM, POS_AIN3|NEG_AINCOM, POS_AIN4|NEG_AINCOM
    EXT5, EXT6, EXT7 = POS_AIN5|NEG_AINCOM, POS_AIN6|NEG_AINCOM, POS_AIN7|NEG_AINCOM

    # You can connect any pin as well to the positive as to the negative ADC input.
    # The following reads the voltage of the potentiometer with negative polarity.
    # The ADC reading should be identical to that of the POTI channel, but negative.
    # POTI_INVERTED = POS_AINCOM|NEG_AIN0

    # For fun, connect both ADC inputs to the same physical input pin.
    # The ADC should always read a value close to zero for this.
    # SHORT_CIRCUIT = POS_AIN0|NEG_AIN0

    # Specify here an arbitrary length list (tuple) of arbitrary input channel pair
    # eight-bit code values to scan sequentially from index 0 to last.
    # Eight channels fit on the screen nicely for this example..
    CH_SEQUENCE = (EXT2, EXT3, EXT4, EXT7)


def reload_config():
    pass


def save_config():
    pass





