# https://towardsdatascience.com/python-webserver-with-flask-and-raspberry-pi-398423cc6f5d
# http://pwp.stevecassidy.net/bottle/forms-processing.html

import json
import time
from random import random
import wtforms
from flask import Flask, render_template, make_response, request, g, flash, url_for

app = Flask(__name__, template_folder='html')


@app.before_request
def before_request():
    g.request_start_time = time.time()
    g.request_time = lambda: "%.5fs" % (time.time() - g.request_start_time)
    g.data_pumpIn = lambda: "%.2fV" % 12
    g.data_pumpOut = lambda: "%.2fV" % 13
    g.data_valveStatus = lambda: "Open"


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/setting')
def setting():
    form = RegistrationForm(request.form)
    return render_template("setting.html", form=form)


@app.route('/graph')
def graph():
    return render_template('index.html')


@app.route('/live-data')
def live_data():
    # Create a PHP array and echo it as JSON
    data = [time.time() * 1000, random() * 100]
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    print(response)
    return response


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
              form.sensorlocation1.data,
              form.sensorlocation2.data,
              form.sensorlocation3.data,
              form.sensorlocation4.data,
              form.sensorlocation5.data,
              form.sensorlocation6.data,
              form.valvelocation1.data,
              form.valvelocation2.data,
              form.valvelocation3.data,
              form.valvelocation4.data,
              form.valvelocation5.data,
              form.valvelocation6.data,
              form.pumplocation1.data,
              form.pumplocation2.data]
    # sc = SaveConstants
    # sc.saveconfig(g.data)
    print(g.data)
    return render_template('setting.html', form=form)


class RegistrationForm(wtforms.Form):
    delta = wtforms.FloatField('Delta', default="0.3")
    activewheels1 = wtforms.BooleanField('Active Wheels 1')
    activewheels2 = wtforms.BooleanField('Active Wheels 2')
    activewheels3 = wtforms.BooleanField('Active Wheels 3')
    activewheels4 = wtforms.BooleanField('Active Wheels 4')
    activewheels5 = wtforms.BooleanField('Active Wheels 5')
    activewheels6 = wtforms.BooleanField('Active Wheels 6')
    sensorlocation1 = wtforms.StringField('Sensor Location 1', [wtforms.validators.Length(min=0, max=3)])
    sensorlocation2 = wtforms.StringField('Sensor Location 2', [wtforms.validators.Length(min=0, max=3)])
    sensorlocation3 = wtforms.StringField('Sensor Location 3', [wtforms.validators.Length(min=0, max=3)])
    sensorlocation4 = wtforms.StringField('Sensor Location 4', [wtforms.validators.Length(min=0, max=3)])
    sensorlocation5 = wtforms.StringField('Sensor Location 5', [wtforms.validators.Length(min=0, max=3)])
    sensorlocation6 = wtforms.StringField('Sensor Location 6', [wtforms.validators.Length(min=0, max=3)])
    valvelocation1 = wtforms.StringField('Valve Location 1', [wtforms.validators.Length(min=0, max=3)])
    valvelocation2 = wtforms.StringField('Valve Location 2', [wtforms.validators.Length(min=0, max=3)])
    valvelocation3 = wtforms.StringField('Valve Location 3', [wtforms.validators.Length(min=0, max=3)])
    valvelocation4 = wtforms.StringField('Valve Location 4', [wtforms.validators.Length(min=0, max=3)])
    valvelocation5 = wtforms.StringField('Valve Location 5', [wtforms.validators.Length(min=0, max=3)])
    valvelocation6 = wtforms.StringField('Valve Location 6', [wtforms.validators.Length(min=0, max=3)])
    pumplocation1 = wtforms.StringField('Pump Location 1', [wtforms.validators.Length(min=0, max=3)])
    pumplocation2 = wtforms.StringField('Pump Location 2', [wtforms.validators.Length(min=0, max=3)])


class SaveConstants:
    def saveconfig(self, data):
        with open('data.txt', 'w') as outfile:
            json.dump(data, outfile, indent=4)

    def loadconfig(self):
        with open('data.txt') as json_file:
            data = json.load(json_file)
        for p in data:
            print(p)
        return data


if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')
