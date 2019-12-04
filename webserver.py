# https://towardsdatascience.com/python-webserver-with-flask-and-raspberry-pi-398423cc6f5d

from flask import Flask, render_template

app = Flask(__name__, template_folder='html')


@app.route('/')
def home():
    x = "home.html"
    return render_template(x)


@app.route('/about/')
def about():
    x = "about.html"
    return render_template(x)


@app.route('/setting/')
def setting():
    x = "setting.html"
    return render_template(x)


if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')
