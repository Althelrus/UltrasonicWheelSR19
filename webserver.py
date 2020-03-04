#!/usr/bin/python
# -*- coding: utf-8 -*-
# https://towardsdatascience.com/python-webserver-with-flask-and-raspberry-pi-398423cc6f5d
# http://pwp.stevecassidy.net/bottle/forms-processing.html
# http://abyz.me.uk/rpi/pigpio/python.html

import json
import os
import time
import wtforms
from flask import Flask, render_template, make_response, request, g
from flaskthreads import AppContextThread
#todo
from ADS1256_definitions import *
from pipyadc import ADS1256

app = Flask(__name__, template_folder='html')
#todo
import pigpio
pi = pigpio.pi()  # Connect to local Pi.

#########################
# todo add calls for other wheels and sensors -> model after live_data()
# todo download any scripts that are from the internet
# todo automate amount of graphs that display on site
# todo make refresh every 30 mins
# todo add button in settings page to update program from git repo -> will call batch script ass a subprocess
# todo -> make sure to lead users to reload page after a loading screen gif
#########################
# Motor PINs
# todo -> have the pins setup in the class on init to pass in pin locations
PUMPIN = 12
PUMPOUT = 5
VALVE1 = 13
VALVE_out = 6
VALVE2 = 33
VALVE3 = 23
VALVE4 = 26
VALVE5 = 13
VALVE6 = 6

# speed = pwm duty cycle, 0 = off, 100 = max
speed = 100
#todo
pi.set_mode(PUMPIN, pigpio.OUTPUT)
pi.set_mode(PUMPOUT, pigpio.OUTPUT)
pi.set_mode(VALVE1, pigpio.OUTPUT)
pi.set_mode(VALVE_out, pigpio.OUTPUT)
pi.set_mode(VALVE3, pigpio.OUTPUT)
pi.set_mode(VALVE4, pigpio.OUTPUT)
pi.set_mode(VALVE5, pigpio.OUTPUT)
pi.set_mode(VALVE6, pigpio.OUTPUT)


# todo fix load
# ->todo try loading
#   ->todo parse loading data
# ->todo try catch
#   ->todo still have the default values in the catch
@app.before_first_request
def start_up():
    print("## First ###")
    # save = SaveConstants()
    # g.loaded_data = save.loadconfig()
    # g.list1 = []
    # for p in g.loaded_data:
    #    g.list1.append(p)
    g.data_pumpIn = lambda: "Off"
    g.data_pumpOut = lambda: "Off"
    g.delta = .2  # This value is used to find the upper and lower bounds of the ideal todo read from data
    g.mode = 1  # This value is to tell in what state the wheel is in
    g.w_act = [1, 0, 0, 0, 0, 0]  # This is the default active wheels todo read from load


# This runs before anything on the page to update anything on the page
# todo fix what we are writing out to the screen
@app.before_request
def before_request():
    g.request_start_time = time.time()
    g.request_time = lambda: "%.5fs" % (time.time() - g.request_start_time)
    g.data_valveStatus = lambda: ' '.join(map(str, g.w_act))
    g.data_pumpIn = lambda: "Off"   # todo test
    g.data_pumpOut = lambda: "Off"  # todo test
    wheels = Wheel()
    volts = wheels.read_sensor()
    g.w_act = str(list(volts))  # This is the default active wheels todo test


# Home page of the website
@app.route('/')
def home():
    return render_template("home.html")


# About page of the website
@app.route('/about')
def about():
    return render_template("about.html")


# Settings page of the website
@app.route('/setting')
def setting():
    form = RegistrationForm(request.form)
    return render_template("setting.html", form=form)


# Test page of the website
# todo remove
@app.route('/graph')
def graph():
    return render_template('index.html')


# Clean up when restarting server, and saving data file
#todo
# add final save
# call reboot script
@app.route('/stop', methods=['POST'])
def stop():
    form = RegistrationForm(request.form)
    return render_template("setting.html", form=form)
    #todo
    #pi.stop()
    #GPIO.cleanup()

# called from webpage -> pressurise the wheel up to 7psi then turn of pumps
# todo pressurise the wheel up to 7psi then turn of pumps
@app.route('/pressurise', methods=['POST'])
def pressurise():
    # todo call pressurization routine
    return render_template("setting.html")

# called from Webpage -> almost drain the entire wheel
# todo almost drain the entire wheel
@app.route('/depressurise', methods=['POST'])
def depressurise():
    # todo call depressurization routine
    return render_template("setting.html")


# for setting the javascript variable on active wheels called from javascripts
@app.route('/act_wheels')
def act_wheels():
    data = g.w_act
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response


# Function called from javascript on the graph in the html
# gets the volts reading
# todo route through pressure function
@app.route('/live-data')
def live_data():
    # Create a PHP array and echo it as JSON
    wheels = Wheel()
    volts = wheels.read_sensor()
    print(volts)
    data = [time.time() * 1000, volts_to_pressure(volts)[1]]
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response


# todo add threading call
# function gets called from javascript
@app.route('/control_motor')
def control_motor():
    wheels = Wheel()
    volts = wheels.read_sensor()
    pressure = volts_to_pressure(volts)
    for x in pressure:
        print(x)
        if pressure[1] == g.ideal:
            print("Good")
            g.data_pumpIn = lambda: "Off"
            g.data_pumpOut = lambda: "Off"
        elif (x - .2) <= g.ideal:
            print("low")
            g.data_pumpIn = lambda: "On"
            g.data_pumpOut = lambda: "Off"
            g.gx = x
            pressure_low()
            #t.start()
            #t.join()
        elif (pressure[1] + .2) >= g.ideal:
            print("high")
            g.data_pumpIn = lambda: "Off"
            g.data_pumpOut = lambda: "On"
            pressure_high()
            #t.start()
            #t.join()
        else:
            g.data_pumpIn = lambda: "Hello"
            g.data_pumpOut = lambda: "World"
    return 'ok'


# This function will continuously remove pressure to the wheel for x of the wheel
#todo
# add ablity to have the pumps vary in speed
def pressure_high():
    wheels = Wheel()
    print("HIGH RUN")
    volts = wheels.read_sensor()
    wheels.control_valve(VALVE1, 0)
    if (volts_to_pressure(wheels)[1]) >= (3.5 - .2 - 0.05):
        print(volts_to_pressure(volts)[1])
        wheels.control_valve(VALVE_out, 1)
        wheels.control_pump(PUMPOUT, 0)
        time.sleep(.01)
        wheels.control_valve(VALVE_out, 1)
        print("HIGH RUN")

    wheels.control_valve(VALVE_out, 0)
    wheels.control_pump(PUMPOUT, 150)


# This function will continuously add pressure to the wheel for x of the wheel
#todo
# add ablity to have the pumps vary in speed
def pressure_low():
    wheels = Wheel()
    print("LOW RUN")
    volts = wheels.read_sensor()
    wheels.control_valve(VALVE_out, 0)
    wheels.control_valve(VALVE1, 1)
    if (volts_to_pressure(volts)[1]) <= (3.5 + .2 - 0.05):
        print(volts_to_pressure(volts)[1])
        wheels.control_pump(PUMPIN, 200)
        print("LOW RUN")
    wheels.control_valve(VALVE1, 0)


# Set Ideal Pressure and converts volts to pressure
#todo
# Add Equtions
def volts_to_pressure(volts):
    print(volts)
    if 1 == 1: #todo Change back
        pressure = list(map(lambda x: -3.636363*(0.6-x), volts))  # returns static and position up
        g.ideal = 3.5
    elif g.mode == 2:
        pressure = list(map(lambda x: x ** 2, volts))  # returns Down force
        g.ideal = 3.7
    elif g.mode == 3:
        pressure = list(map(lambda x: x ** 2, volts))  # returns moving
        g.ideal = 2.5
    else:
        pressure = list(map(lambda x: x, volts))  # returns volts
        g.ideal = 3.5
    return pressure


# this is called when someone submits anything in settings
# todo save data in here
@app.route('/setting_data', methods=['GET', 'POST'])
def setting_data():
    form = RegistrationForm(request.form)
    g.data = [form.delta.data,
              form.activewheels1.data,
              form.activewheels2.data,
              form.activewheels3.data,
              form.activewheels4.data,
              form.activewheels5.data,
              form.activewheels6.data,
              form.valvelocation1.data,
              form.valvelocation2.data,
              form.valvelocation3.data,
              form.valvelocation4.data,
              form.valvelocation5.data,
              form.valvelocation6.data,
              form.pumplocation1.data,
              form.pumplocation2.data]
    print(g.data)
    return render_template('setting.html', form=form)

#todo complete-remove
# This Class makes the Registration Form
class RegistrationForm(wtforms.Form):
    delta = wtforms.FloatField('Delta', default="0.3")
    activewheels1 = wtforms.BooleanField('Active Wheels 1', default=True)
    activewheels2 = wtforms.BooleanField('Active Wheels 2')
    activewheels3 = wtforms.BooleanField('Active Wheels 3')
    activewheels4 = wtforms.BooleanField('Active Wheels 4')
    activewheels5 = wtforms.BooleanField('Active Wheels 5')
    activewheels6 = wtforms.BooleanField('Active Wheels 6')
    valvelocation1 = wtforms.StringField('Valve Location 1', [wtforms.validators.Length(min=0, max=3)], default="25")
    valvelocation2 = wtforms.StringField('Valve Location 2', [wtforms.validators.Length(min=0, max=3)], default="33")
    valvelocation3 = wtforms.StringField('Valve Location 3', [wtforms.validators.Length(min=0, max=3)], default="23")
    valvelocation4 = wtforms.StringField('Valve Location 4', [wtforms.validators.Length(min=0, max=3)], default="24")
    valvelocation5 = wtforms.StringField('Valve Location 5', [wtforms.validators.Length(min=0, max=3)], default="13")
    valvelocation6 = wtforms.StringField('Valve Out Location', [wtforms.validators.Length(min=0, max=3)], default="24")
    pumplocation1 = wtforms.StringField('Pump In Location 1', [wtforms.validators.Length(min=0, max=3)], default="16")
    pumplocation2 = wtforms.StringField('Pump Out Location 2', [wtforms.validators.Length(min=0, max=3)], default="12")


# This Class Communicates with all of the sensors and pumps
# todo complete- remove
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


# This Saves and loads the config
# todo move to separate file
class SaveConstants:
    def saveconfig(self, data):
        with open('/home/pi/Desktop/UltrsonicWheelSR19/data.txt', 'w') as outfile:
            json.dump(data, outfile, indent=4)

    def loadconfig(self):
        print("load")
        with open('/home/pi/Desktop/UltrsonicWheelSR19/data.txt') as json_file:
            data = json.load(json_file)
        return data


# Starts the Web application on the hostname
if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')
