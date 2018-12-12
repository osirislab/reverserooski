from flask_wtf import FlaskForm
from wtforms.fields import TextField, SubmitField
from wtforms.validators import Required

class RegisterClientForm(FlaskForm):
    hostname = TextField('hostname', validators=[Required()])
    uname = TextField('uname', validators=[Required()])
