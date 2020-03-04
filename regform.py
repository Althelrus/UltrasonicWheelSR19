
import wtforms

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