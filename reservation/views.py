# Display reservation view for guest
# Yousef Alahrbi
# 10/25/2016


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
			date_in=form.date_in.data,
			date_out=form.date_out.data,
			members=form.members.data
			)
		# if search:
		# 	session['date_in'] = form.date_in.data
		# 	session['date_out'] = form.date_out.data

		if form.date_in.data >= form.date_out.data:
			flash ("Please Enter a Valid date")
		else:
			return redirect(url_for('results'))
		db.session.add(search)
		db.session.commit()
	return render_template('reservation/search.html', form = form)


@app.route('/results', methods=('GET', 'POST'))
def results():
	# if Room.query.filter_by(booked_from == None).first():
	# 	sql_search = text('select distinct(room_id), room_type, room_num, price from room join search where (date_in = book_release) or (date_in > book_release)')
	# 	result_ = db.engine.execute(sql_search)
	# 	return redirect(url_for('results', result=result_))
	# result_ch = Room.query.filter_by(state=True).first()
	# if result_ch:
	# 	result = Room.query.filter_by(state=True).first()
	# 	return redirect(url_for('results', result=result))
	# else:
	sql_search = text('select distinct(room_id), room_type, room_num, price from room join search where (date_in = book_release) or (date_in > book_release)')
	result_ = db.engine.execute(sql_search)
		# return redirect(url_for('results', result=result_))


	return render_template('reservation/result.html', result = result_)	


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
			room = Room.query.filter_by(room_id=session['room_id']).first(),
			first_name=form.first_name.data,
			last_name=form.last_name.data,
			date_in=form.date_in.data,
			date_out=form.date_out.data,
			# date_in = Search.query.filter_by(date_in=session['date_in']).first(),
			# date_out = Search.query.filter_by(date_out=session['date_in']).first(),
			members=form.members.data,
			email=form.email.data,
			phone_num=form.phone_num.data,
			address=form.address.data,
			city=form.city.data,
			state=form.state.data,
			zip_code=form.zip_code.data,
			# False,
			# False
			)
		# date_in = Search.query.filter_by(date_in=session['date_in']).first()
		# date_out = Search.query.filter_by(date_out=session['date_in']).first()
		room = Room.query.filter_by(room_id=session['room_id']).first()
		room.booked_from = form.date_in.data
		room.book_release = form.date_out.data

		db.session.flush()
		db.session.add(reservation)
		db.session.commit()


		
		# db.session.commit()
		return redirect('/reserve_guest')
	return render_template('reservation/reserv.html', form = form)

	
@app.route('/reserve_guest')
def reserve_guest():

	return "All done"



@app.route("/index")
def index():
	return "Hello World"









