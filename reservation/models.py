# Create database for reservation 
# Yousef Alharbi
# 10/28/2016


# add libraries
from Magnet import db


class Search(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	date_in = db.Column(db.Date)
	date_out = db.Column(db.Date)
	members = db.Column(db.Integer)
	

	def __init__(self,date_in,date_out,members):
		self.date_in = date_in
		self.date_out = date_out
		self.members = members 

#create table for reservation
class Reservation(db.Model):

	reservation_id = db.Column(db.Integer, primary_key = True)
	room_num = db.Column(db.Integer, db.ForeignKey('room.room_num'))
	first_name = db.Column(db.String(80))
	last_name = db.Column(db.String(80))
	date_in = db.Column(db.Date)
	date_out = db.Column(db.Date)
	members = db.Column(db.String(10))
	email = db.Column(db.String(80))
	phone_num = db.Column(db.String(20))
	address = db.Column(db.String(80))
	city = db.Column(db.String(80))
	state = db.Column(db.String(80))
	zip_code = db.Column(db.String(20))
	check_in = db.Column(db.Boolean)
	check_out = db.Column(db.Boolean)


	def __init__(self,room,first_name,last_name,date_in,date_out,members,email,phone_num,address,city,state,zip_code, check_in = False, check_out = False):
		self.first_name = first_name
		self.room_num = room.room_num
		self.last_name = last_name
		self.date_in = date_in
		self.date_out = date_out
		self.members = members
		self.email = email
		self.phone_num = phone_num
		self.address = address
		self.city = city
		self.state = state
		self.zip_code = zip_code
		self.check_in = check_in
		self.check_out = check_out
	def __repr__(self):
		return '<Reservation %r>' % self.last_name


#create table for room
class Room(db.Model):
	room_num = db.Column(db.Integer, primary_key= True)
	room_type = db.Column(db.String(40))
	status = db.Column(db.Boolean)
	# price = db.Column(db.Numeric(6,2))
	price = db.Column(db.Float)
	book_from = db.Column(db.Date)
	book_release = db.Column(db.Date)
	reserved = db.relationship('Reservation', backref='room', lazy='dynamic')
	

	def __init__(self,room_num,room_type,status,price):
		self.room_num = room_num
		self.room_type = room_type
		self.status = status
		self.price = price

	def __repr__(self):
		return '<Room %r>' % self.room_num



# class Reserved(db.Model):
# 	id = db.Column(db.Integer, primary_key = True)
# 	reserve_id = db.Column(db.Integer, db.ForeignKey('reservation.reservation_id'))
# 	# room_id = db.Column(db.Integer, db.ForeignKey('room.room_id'))
# 	# first_name = db.Column(db.String(40), db.ForeignKey('reservation.first_name'))

# 	def __init__(self,reservation,room):
# 		self.reserve_id = reservation.reservation_id
		# self.room_id = room.room_id
		# self.first_name = reservation.first_name

#room id should be in reserved 
#reservation id should be in reserved







