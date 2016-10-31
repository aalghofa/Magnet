# Display reservation view for guest
# Yousef Alahrbi
# 10/29/2016


# add libraries
from Magnet import app, db
from flask import render_template, redirect, session, request, url_for, flash
from reservation.form import SearchForm, ReservationForm, AddRoomForm
from reservation.models import Search, Reservation, Room
from datetime import date
from sqlalchemy import text


#add routes
@app.route('/', methods=('GET', 'POST'))
def search():
	form = SearchForm()
	if form.validate_on_submit():
		search = Search(
			form.date_in.data,
			form.date_out.data,
			form.members.data
			)
		if form.date_in.data >= form.date_out.data:
			flash ("Please enter a valid date")
		else:
			db.session.add(search)
			db.session.commit()
			result = Room.query.filter(Room.book_release <= search.date_in).all()
			return render_template('reservation/result.html', result = result)
			return redirect('/results')
		
	return render_template('reservation/search.html', form = form)

	
@app.route('/results', methods=('GET', 'POST'))
def results():
	return('in results')

	# sql_search = text('select distinct(room_id), room_type, room_num, price from room join search where date_in <= book_release or status = True ')
	# result_ = db.engine.execute(sql_search)
	
	# return render_template('reservation/result.html', result = result_)

@app.route('/book/<int:room_id>')
def book(room_id):
    room = Room.query.filter_by(room_id=room_id).first_or_404()
    session['room_id'] = room_id
    room.status = False
    db.session.commit()
    return redirect('/reserv')

@app.route('/addroom', methods=('GET', 'POST'))
def addroom():
	form = AddRoomForm()
	if form.validate_on_submit():
		room = Room(
			form.room_num.data,
			form.room_type.data,
			True,
			form.price.data
			)	
		db.session.add(room)
		db.session.commit()
		return redirect('/')
	return render_template('reservation/addroom.html', form = form)
    

@app.route('/reserv', methods=('GET', 'POST'))
def reserv():
	form = ReservationForm()
	if form.validate_on_submit():
		reservation = Reservation(
			Room.query.filter_by(room_id=session['room_id']).first(),
			form.first_name.data,
			form.last_name.data,
			form.date_in.data,
			form.date_out.data,
			form.members.data,
			form.email.data,
			form.phone_num.data,
			form.address.data,
			form.city.data,
			form.state.data,
			form.zip_code.data,
			False,
			False
			)
		room = Room.query.filter_by(room_id = session['room_id']).first()
		room.book_from = form.date_in.data
		room.book_release = form.date_out.data
		db.session.commit()

		db.session.add(reservation)
		db.session.commit()
		return redirect('/reserve_guest')
	return render_template('reservation/reserv.html', form = form)

	
@app.route('/reserve_guest')
def reserve_guest():
	return "All done"



@app.route("/index")
def index():

	result1 = Reservation.query.filter(Reservation.check_in == False).filter_by(date_in = date.today()).all()
	result2 = Reservation.query.filter(Reservation.check_out == False).filter_by(date_out = date.today()).all()

	return render_template('reservation/index.html', result1 = result1, result2 = result2)

@app.route('/check_in/<int:reservation_id>')
def check_in(reservation_id):
	reservation = Reservation.query.filter_by(reservation_id = reservation_id).first()
	reservation.check_in = True
	reservation.check_out = False
	db.session.commit()
	flash('guest checked in')
	return redirect('index')

@app.route('/check_out/<int:reservation_id>')
def check_out(reservation_id):
	reservation = Reservation.query.filter_by(reservation_id = reservation_id).first()
	reservation.check_out = True
	db.session.commit()
	flash('guest checked out')
	return redirect('index')










