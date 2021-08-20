from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, HiddenField
from wtforms import IntegerField, SelectField
from wtforms.validators import InputRequired, Email, Length, EqualTo
from wtforms_components import DateField
from datetime import date
from Utils.variables import groups
from Utils.validators import FormAccountValidator

fav = FormAccountValidator


class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(),
                            Length(min=4, max=31), fav(opt='user')])
    password = PasswordField('password', validators=[InputRequired(),
                            Length(min=6, max=128), fav(opt='password')])
    remember = BooleanField('remember me')


class UsersForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(),
                            Length(min=4, max=31), fav(opt='user')])
    group = SelectField(u'Group', choices=groups)
    password = PasswordField('password', validators=[InputRequired(), Length(min=6, max=128),
                fav(opt='password'), EqualTo('pwconfirm', message='Passwords must match')])
    pwconfirm = PasswordField('Repeat Password')
    delete = HiddenField('Delete', default='N', validators=[Length(max=1)])


class UsersFormEdit(FlaskForm):
    username = StringField('Usersname', validators=[InputRequired(),
                Length(min=4, max=31), fav(opt='user')])
    group = SelectField(u'Group', choices=groups)
    delete = HiddenField('Delete', default='N', validators=[Length(max=1)])


class UsersFormPassword(FlaskForm):
    password = PasswordField('New Password', validators=[InputRequired(), fav(opt='password'),
        Length(min=6, max=128),EqualTo('pwconfirm', message='Passwords must match')])
    pwconfirm = PasswordField('Repeat New Password')
    uid = HiddenField('UserID')



