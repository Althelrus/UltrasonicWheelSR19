
from ADS1256_definitions import *
from pipyadc import ADS1256

import pigpio
pi = pigpio.pi()  # Connect to local Pi.

PUMPIN = 12
PUMPOUT = 5
VALVE1 = 13
VALVE_out = 6
VALVE2 = 33
VALVE3 = 23
VALVE4 = 26
VALVE5 = 13
VALVE6 = 6

pi.set_mode(PUMPIN, pigpio.OUTPUT)
pi.set_mode(PUMPOUT, pigpio.OUTPUT)
pi.set_mode(VALVE1, pigpio.OUTPUT)
pi.set_mode(VALVE_out, pigpio.OUTPUT)
pi.set_mode(VALVE3, pigpio.OUTPUT)
pi.set_mode(VALVE4, pigpio.OUTPUT)
pi.set_mode(VALVE5, pigpio.OUTPUT)
pi.set_mode(VALVE6, pigpio.OUTPUT)

class Wheel:
    def read_sensor(self):
        ads = ADS1256()
        ads.cal_self()
        POTI = POS_AIN0|NEG_AINCOM
        EXT2, EXT3, EXT4 = POS_AIN2 | NEG_AINCOM, POS_AIN3 | NEG_AINCOM, POS_AIN4 | NEG_AINCOM
        EXT5, EXT6, EXT7 = POS_AIN5 | NEG_AINCOM, POS_AIN6 | NEG_AINCOM, POS_AIN7 | NEG_AINCOM
        CH_SEQUENCE = (EXT2, EXT3, EXT4, EXT7)
        raw_channels = ads.read_sequence(CH_SEQUENCE)
        voltages = [i * ads.v_per_digit for i in raw_channels]
        return voltages

    def control_valve(self, location, value):
        pi.write(location, value)

    def control_pump(self, location, dutyratio):
        pi.set_PWM_dutycycle(location, dutyratio)