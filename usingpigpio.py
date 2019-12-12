#!/usr/bin/env python

from flask import Flask, render_template

# Initialize the Flask application
app = Flask(__name__)

import pigpio

pi = pigpio.pi()  # Connect to local Pi.

#########################
# Motor PINs
PUMPIN = 12  # left fwd
PUMPOUT = 16  # left rev
VALVE1 = 23  # right fwd
VALVE2 = 22  # right rev
VALVE3 = 24
VALVE4 = 27
VALVE5 = 17
VALVE6 = 25

# speed = pwm duty cycle, 0 = off, 100 = max
speed = 100

# (1,1) = fwd, (2,2) = rev, (1,2) = left, (0,0) = right, (1,0) = fwd left, (0,1) = fwd right, (2,0) = rev left, (0,2) = rev right
current_direction = (0, 0)

# setup gpios

pi.set_mode(PUMPIN, pigpio.OUTPUT)
pi.set_mode(PUMPOUT, pigpio.OUTPUT)
pi.set_mode(VALVE1, pigpio.OUTPUT)
pi.set_mode(VALVE2, pigpio.OUTPUT)


# Route '/' and '/index' to `index`
@app.route('/')
@app.route('/index')
def index():
    # Render template
    return render_template('index.html')


@app.route('/<int:id1>/<int:id2>')
def article(id1, id2):
    global current_direction
    global speed
    # current_direction = (id1, id2)
    # (1,1) = fwd, (2,2) = rev, (1,2) = left, (0,0) = right, (1,0) = fwd left, (0,1) = fwd right, (2,0) = rev left, (0,2) = rev right
    if (id1 >= 0 and id1 <= 2 and id2 >= 0 and id2 <= 2):
        print
        'id1 is = >>> ' + str(id1) + ' - id2 is = >>> ' + str(id2)
        current_direction = (id1, id2)
    elif (id1 == 3 and id2 == 10):  ## low speed
        speed -= 10
        if speed < 0:
            speed = 0
        print
        "Speed : " + str(speed) + "\n"
        ################################
    # elif (id1 == 3 and id2 == 20):
    #   print 'id is >>> ' + str (id2)
    ################################
    elif (id1 == 3 and id2 == 15):  ## high speed
        speed += 10
        if speed > 100:
            speed = 100
        print
        "Speed : " + str(speed) + "\n"
        ################################
    else:
        current_direction = (0, 0)
    # time.sleep(.2)
    motor_change()
    return render_template('index.html', title=id2)


@app.route('/stop')
def stopgpio():
    pi.stop()


def motor_change():
    # motor 1
    if (current_direction[0] == 1):
        pi.set_PWM_dutycycle(MOTOR1A, speed)
        pi.set_PWM_dutycycle(MOTOR1B, 0)
    elif (current_direction[0] == 2):
        pi.set_PWM_dutycycle(MOTOR1A, 0)
        pi.set_PWM_dutycycle(MOTOR1B, speed)
    # if 0 (stop) or invalid stop anyway
    else:
        pi.set_PWM_dutycycle(MOTOR1A, 0)
        pi.set_PWM_dutycycle(MOTOR1B, 0)
    # motor 2
    if (current_direction[1] == 1):
        pi.set_PWM_dutycycle(MOTOR2A, speed)
        pi.set_PWM_dutycycle(MOTOR2B, 0)
    elif (current_direction[1] == 2):
        pi.set_PWM_dutycycle(MOTOR2A, 0)
        pi.set_PWM_dutycycle(MOTOR2B, speed)
    # if 0 (stop) or invalid stop anyway
    else:
        pi.set_PWM_dutycycle(MOTOR2A, 0)
        pi.set_PWM_dutycycle(MOTOR2B, 0)

    # Run


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=True)