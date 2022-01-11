from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, HiddenField
from wtforms import IntegerField, SelectField
from wtforms.validators import InputRequired, Email, Length, EqualTo
from wtforms.validators import IPAddress
from wtforms_components import DateField
from datetime import date
from Utils.validators import FormIpValidator
from Utils.variables import pf

fiv = FormIpValidator


class NetifForm(FlaskForm):
    address_family = SelectField(u'Address Family', choices=pf['af'])
    ip = StringField(u'IP address', validators=[InputRequired(),
                            IPAddress()])

