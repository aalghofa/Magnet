# Create database for reservation 
# Yousef Alharbi
# 10/19/2016


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


##create a virtual table that does not appear in the database, it only exists to link the room to reservation
reserved = db.Table('reserved', 
	db.Column('reservation_id', db.Integer, db.ForeignKey('reservation.reservation_id')),
	db.Column('room_id', db.Integer, db.ForeignKey('room.room_id'))

	)

#create table for reservation
class Reservation(db.Model):
	reservation_id = db.Column(db.Integer, primary_key = True)
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

	reserved = db.relationship('Room',secondary=reserved, backref=db.backref('guest', lazy='dynamic'))

	def __init__(self,first_name,last_name,date_in,date_out,members,email,phone_num,address,city,state,zip_code):
		self.first_name = first_name
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

	def __repr__(self):
		return '<Reservation %r>' % self.last_name


#create table for room
class Room(db.Model):
	room_id = db.Column(db.Integer, primary_key = True)
	room_num = db.Column(db.String(30), unique = True)
	room_type = db.Column(db.String(40))
	status = db.Column(db.Boolean)
	price = db.Column(db.Numeric(6,2))
	# rooms = db.relationship('Reserved', backref = 'room', lazy = 'dynamic')
	def __init__(self,room_num,room_type,status,price):
		self.room_num = room_num
		self.room_type = room_type
		self.status = status
		self.price = price

	def __repr__(self):
		return '<Room %r>' % self.room_type


# class Reserved(db.Model):
# 	id = db.Column(db.Integer, primary_key = True)
# 	reserve_id = db.Column(db.Integer, db.ForeignKey('reservation.id'))
# 	# room_id = db.Column(db.Integer, db.ForeignKey('room.id'))



#room id should be in reserved 
#reservation id should be in reserved







