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
def about():
    x = "setting.html"
    return render_template(x)


if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')

# form = '''
#                < form action = "post.html" method = "post" >
#                    <input type="text" name="name"></input>
#                    <input type="radio" name="topping" value="supreme">Supreme</input>
#                    <input type="radio" name="topping" value="vegetarian">Vegetarian</input>
#                    <input type="radio" name="topping" value="hawaiian">Hawaiian</input>
#                    <select name="sauce">
#                      <option value="tomato">Tomato</option>
#                      <option value="barbeque">Barbeque</option>
#                     <option value="mayonnaise">Mayonnaise</option>
#                      <option value="secret">Secret Sauce</option>
#                 <option selected="selected" value="secret">Secret Sauce</option>
#                 <input type="checkbox" name="extra_cheese" value="1">Extra Cheese</input>
#                <input type="checkbox" name="gluten_free" value="1">Gluten Free Base</input>
#               <input type="checkbox" name="extras" value="extra_cheese">Extra Cheese</input>
#              <input type="checkbox" name="extras" value="gluten_free">Gluten Free Base</input>
#             <input type="checkbox" name="extras" value="extra_cheese">Extra Cheese</input>
#            <input type="checkbox" name="extras" value="gluten_free">Gluten Free Base</input>
# '''
# return "<BR>" + "header /n" + form + "<BR>"
