# https://towardsdatascience.com/python-webserver-with-flask-and-raspberry-pi-398423cc6f5d

import json
from time import time
from random import random
from flask import Flask, render_template, make_response


app = Flask(__name__, template_folder='html')


@app.route('/')
def home():
    return render_template("home.html", data='test')


@app.route('/about_application/')
def about():
    return render_template("about.html", data='test')


@app.route('/setting/')
def setting():
    return render_template("setting.html", data='test')


@app.route('/graph/')
def graph():
    return render_template('index.html', data='test')


@app.route('/live-data')
def live_data():
    # Create a PHP array and echo it as JSON
    data = [time() * 1000, random() * 100]
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response


if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')
