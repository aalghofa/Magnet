# This the form to set reservation form
# Yousef Alharbi
# 10/16/2016


# add libraries
from flask_wtf import Form
from wtforms import validators, StringField, PasswordField
from wtforms.fields.html5 import EmailField, DateField, IntegerField


class SearchForm(Form):
	date_in = DateField('Check in', [validators.Required()])
	date_out = DateField('Check out', [validators.Required()])
	members = IntegerField('members', [validators.Required()])

class AddRoomForm(Form):
	room_num = StringField('room_num', [validators.Required()])
	room_type = StringField('room_type', [validators.Required()])
	price = IntegerField('price', [validators.Required()])


#set class for reservation form
class ReservationForm(Form):
	first_name = StringField('First Name', [validators.Required()])
	last_name = StringField('Last Name', [validators.Required()])
	date_in = DateField('Check in', [validators.Required()])
	date_out = DateField('Check out', [validators.Required()])
	members = StringField('Members')
	email = EmailField('Email',[validators.Required()])
	phone_num = StringField('Phone number',[validators.Required()])
	address = StringField('Address',[validators.Required()])
	city = StringField('City',[validators.Required()])
	state = StringField('State',[validators.Required()])
	zip_code = StringField('Zip-code',[validators.Required()])


