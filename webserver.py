# https://towardsdatascience.com/python-webserver-with-flask-and-raspberry-pi-398423cc6f5d
# http://pwp.stevecassidy.net/bottle/forms-processing.html

import json
import time
from random import random
import wtforms
from bottle import redirect
from flask import Flask, render_template, make_response, request, g, flash, url_for

app = Flask(__name__, template_folder='html')


@app.before_request
def before_request():
    g.request_start_time = time.time()
    g.request_time = lambda: "%.5fs" % (time.time() - g.request_start_time)
    g.data_pumpIn = lambda: "%.2fV" % 12
    g.data_pumpOut = lambda: "%.2fV" % 13
    g.data_valveStatus = lambda: "True"


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/setting_data')
def setting_data():
    # data = [request.form['input'], request.form['input1'], request.form['input2'],
     #       request.form['input3'], request.form['input4'], request.form['input5']
     #       , request.form['input6'], request.form['input7'], request.form['input8'],  request.form['input9']
     #       , request.form['input10'], request.form['input11'], request.form['input12'],  request.form['input13']
     #       , request.form['input14'], request.form['checkbox[]']]
    # response = make_response(json.dumps(data))
    # response.content_type = 'application/json'
    # print(response)
    # return response
    return 1


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


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        flash('Thanks for registering')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


class RegistrationForm(wtforms.Form):
    delta = wtforms.IntegerField('Delta')
    activewheels1 = wtforms.BooleanField('Active Wheels')
    activewheels2 = wtforms.BooleanField('Active Wheels')
    activewheels3 = wtforms.BooleanField('Active Wheels')
    activewheels4 = wtforms.BooleanField('Active Wheels')
    activewheels5 = wtforms.BooleanField('Active Wheels')
    activewheels6 = wtforms.BooleanField('Active Wheels')
    sensorlocation1 = wtforms.StringField('Sensor Location', [wtforms.validators.Length(min=0, max=3)])
    sensorlocation2 = wtforms.StringField('Sensor Location', [wtforms.validators.Length(min=0, max=3)])
    sensorlocation3 = wtforms.StringField('Sensor Location', [wtforms.validators.Length(min=0, max=3)])
    sensorlocation4 = wtforms.StringField('Sensor Location', [wtforms.validators.Length(min=0, max=3)])
    sensorlocation5 = wtforms.StringField('Sensor Location', [wtforms.validators.Length(min=0, max=3)])
    sensorlocation6 = wtforms.StringField('Sensor Location', [wtforms.validators.Length(min=0, max=3)])
    valvelocation1 = wtforms.StringField('Valve Location', [wtforms.validators.Length(min=0, max=3)])
    valvelocation2 = wtforms.StringField('Valve Location', [wtforms.validators.Length(min=0, max=3)])
    valvelocation3 = wtforms.StringField('Valve Location', [wtforms.validators.Length(min=0, max=3)])
    valvelocation4 = wtforms.StringField('Valve Location', [wtforms.validators.Length(min=0, max=3)])
    valvelocation5 = wtforms.StringField('Valve Location', [wtforms.validators.Length(min=0, max=3)])
    valvelocation6 = wtforms.StringField('Valve Location', [wtforms.validators.Length(min=0, max=3)])
    pumplocation1 = wtforms.StringField('Pump Location', [wtforms.validators.Length(min=0, max=3)])
    pumplocation2 = wtforms.StringField('Pump Location', [wtforms.validators.Length(min=0, max=3)])


if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')
