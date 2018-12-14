from flask_wtf import FlaskForm
from wtforms.fields import TextField, SubmitField
from wtforms.validators import Required

class RegisterClientForm(FlaskForm):
    clientname = TextField('clientname', validators=[Required()])
    uname = TextField('uname', validators=[Required()])

class PingForm(FlaskForm):
    clientid=TextField('clientid', validators=[Required()])
