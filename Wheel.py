#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
from ADS1256_definitions import *
import pigpio

PUMPIN = 12
PUMPOUT = 5
VALVE1 = 13
VALVE_out = 6




class Sensor:
    def __init__(self):
        from pipyadc import ADS1256
        POTI = POS_AIN0 | NEG_AINCOM
        EXT2, EXT3, EXT4 = POS_AIN2 | NEG_AINCOM, POS_AIN3 | NEG_AINCOM, POS_AIN4 | NEG_AINCOM
        EXT5, EXT6, EXT7 = POS_AIN5 | NEG_AINCOM, POS_AIN6 | NEG_AINCOM, POS_AIN7 | NEG_AINCOM
        self.CH_SEQUENCE = (EXT2, EXT3, EXT4, EXT7)
        self.ads = ADS1256()
        self.ads.cal_self()
        print("Sensor Init")

    def read_sensor(self):
        raw_channels = self.ads.read_sequence(self.CH_SEQUENCE)
        voltages = [i * self.ads.v_per_digit for i in raw_channels]
        return voltages

class Wheel:
    def __init__(self):
        self.pi = pigpio.pi()  # Connect to local Pi.
        self.pi.set_mode(PUMPIN, pigpio.OUTPUT)
        self.pi.set_PWM_dutycycle(PUMPIN, 0)
        time.sleep(1)
        self.pi.set_mode(PUMPOUT, pigpio.OUTPUT)
        self.pi.set_PWM_dutycycle(PUMPOUT, 0)
        time.sleep(1)
        self.pi.set_mode(VALVE1, pigpio.OUTPUT)
        self.pi.write(VALVE1, 1)
        time.sleep(1)
        self.pi.set_mode(VALVE_out, pigpio.OUTPUT)
        self.pi.write(VALVE_out, 0)
        time.sleep(1)
        print("Wheel Init")

    def control_valve(self, location, value):
        self.pi.write(location, value)

    def control_pump(self, location, dutyratio):
        self.pi.set_PWM_dutycycle(location, dutyratio)

# Test
if __name__ == '__main__':
    s = Sensor()
    w = Wheel()
    for x in range(100):
        voltages = s.read_sensor()
        print(voltages)
        w.control_valve(VALVE1, 1)
        w.control_pump(PUMPIN, 255)
        time.sleep(1)
        voltages = s.read_sensor()
        print(voltages)
        time.sleep(1)
        voltages = s.read_sensor()
        print(voltages)
        time.sleep(1)
        voltages = s.read_sensor()
        print(voltages)
        time.sleep(1)
        voltages = s.read_sensor()
        print(voltages)
        w.control_valve(VALVE1, 0)
        w.control_pump(PUMPIN, 0)
        time.sleep(5)
