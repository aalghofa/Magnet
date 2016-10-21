from flask_wtf import Form
from wtforms import validators, StringField, PasswordField
from wtforms.fields.html5 import EmailField, DateField, IntegerField

class RegisterForm(Form):
    fullname = StringField('Full Name', [validators.Required()])
    username = StringField('Username', [
            validators.Required(),
            validators.Length(min=4, max=25)
        ])
    ssn = IntegerField('ssn', [validators.Required()])
    email = EmailField('Email', [
            validators.Required(),
            validators.Length(min=8, max=25)
        ])
    DOB = DateField('Date of Birth', [validators.Required()])
    job_title = StringField('Job title', [
            validators.Required(),
            validators.Length(min=4, max=20)
        ])
    password = PasswordField('New Password', [
            validators.Required(),
            validators.EqualTo('confirm', message='Passwords must match'),
            validators.Length(min=4, max=80)
        ])
    confirm = PasswordField('Repeat Password')


class LoginForm(Form):
    username = StringField('Username', [
            validators.Required(),
            validators.Length(min=4, max=25)
        ])
    password = PasswordField('New Password', [
            validators.Required(),
            validators.Length(min=4, max=80)
        ])

