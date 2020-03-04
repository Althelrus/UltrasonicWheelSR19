#!/usr/bin/python
# -*- coding: utf-8 -*-
import time

PUMPIN = 12
PUMPOUT = 5
VALVE1 = 13
VALVE_out = 6




class Sensor:
    def __init__(self):
        from ADS1256_definitions import *
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
        import pigpio
        self.pi = pigpio.pi()  # Connect to local Pi.
        self.pi.set_mode(PUMPIN, pigpio.OUTPUT)
        self.pi.write(PUMPIN, 0)
        time.sleep(1)
        self.pi.set_mode(PUMPOUT, pigpio.OUTPUT)
        self.pi.write(PUMPOUT, 0)
        time.sleep(1)
        self.pi.set_mode(VALVE1, pigpio.OUTPUT)
        self.pi.write(VALVE1, 0)
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
    sensors = Sensor.__init__()
    wheels = Wheel.__init__()
    voltages = sensors.read_sensor()
    print(voltages)
    wheels.control_valve(VALVE1, 1)
    wheels.control_pump(PUMPIN, 255)
    time.sleep(1)
    voltages = sensors.read_sensor()
    print(voltages)
    time.sleep(1)
    voltages = sensors.read_sensor()
    print(voltages)
    time.sleep(1)
    voltages = sensors.read_sensor()
    print(voltages)
    time.sleep(1)
    voltages = sensors.read_sensor()
    print(voltages)
    wheels.control_valve(VALVE1, 0)
    wheels.control_pump(PUMPIN, 0)