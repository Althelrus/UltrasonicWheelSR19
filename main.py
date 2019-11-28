# https://www.waveshare.com/wiki/High-Precision_AD/DA_Board


import RPi.GPIO as IO          #calling header file which helps us use GPIO’s of PI

import time                            #calling time to provide delays in program

IO.setwarnings(False)           #do not show any warnings

IO.setmode (IO.BCM)         #we are programming the GPIO by BCM pin numbers. (PIN35 as ‘GPIO19’)

IO.setup(19,IO.OUT)           # initialize GPIO19 as an output.

p = IO.PWM(19,100)          #GPIO19 as PWM output, with 100Hz frequency
p.start(0)                              #generate PWM signal with 0% duty cycle

while 1:                               #execute loop forever

    for x in range (50):                          #execute loop for 50 times, x being incremented from 0 to 49.
        p.ChangeDutyCycle(x)               #change duty cycle for varying the brightness of LED.
        time.sleep(0.1)                           #sleep for 100m second
      
    for x in range (50):                         #execute loop for 50 times, x being incremented from 0 to 49.
        p.ChangeDutyCycle(50-x)        #change duty cycle for changing the brightness of LED.
        time.sleep(0.1)                          #sleep for 100m second

        
        
        
class wheel():
    def wheel():
        valves = {} #Holds the pin location to control the valves objects
        sensors = {} #Holds the pin locations for the sensors objects
        pump = {} #Holds the two pumps objects these objects are made up of direction and pin value
    
    def read_sensor(sensor_location):
    pass

    def control_valve(valve_location):
    pass

    def control_pump(pump_location, voltage):
    pass
    
    
    
class GUI():
  def run_web_Ui(): #make threadable
  pass

    
def main(): #make threadable
    upper_threshold = 3.4
    lower_threshold = 3.6
pass

def reload_config():
pass

def save_config():
pass





# 1 sensor def
# 2 pump def
# Web ui class
# load unload config class
# set variables
