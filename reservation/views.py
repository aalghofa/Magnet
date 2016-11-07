# Display reservation view for guest
# Yousef Alahrbi
# 10/29/2016


# add libraries
from Magnet import app, db, mail
from flask import render_template, redirect, session, request, url_for, flash
from reservation.form import SearchForm, ReservationForm, AddRoomForm
from reservation.models import Search, Reservation, Room
from reservation.decorators import login_required, admin_required
from datetime import date
from sqlalchemy import text
from flask_mail import Mail, Message


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
		first_check = Room.query.filter_by(status = True).all()
		second_check = Room.query.filter(Room.book_release <= search.date_in).all()
		third_check = Room.query.filter(Room.book_release > search.date_in).all()

		#if date is not correct
		if form.date_in.data >= form.date_out.data:
			flash ("Please enter a valid date")

		#if all the rooms are avalible	
		elif first_check:
			result_sta = Room.query.filter_by(status=True).order_by(Room.room_num.desc())
			return render_template('reservation/result.html', result = result_sta)

		# if there are no rooms availble
		elif third_check:
			flash ("No rooms available, Please Select another date")


		#condtions to be satisfied 
		elif second_check:
			result = Room.query.filter(Room.book_release <= search.date_in).all()
			return render_template('reservation/result.html', result = result)


		

			db.session.add(search)
			db.session.commit()
		
	return render_template('reservation/search.html', form = form)


@app.route('/book/<int:room_num>')
def book(room_num):
    room = Room.query.filter_by(room_num=room_num).first_or_404()
    session['room_num'] = room_num
    room.status = False
    db.session.commit()
    return redirect('/reserv')


@app.route('/addroom', methods=('GET', 'POST'))
@login_required
@admin_required
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
		flash ("Room is successfully added")
		return redirect('addroom')
	return render_template('addroom.html', form = form)
    

@app.route('/reserv', methods=('GET', 'POST'))
def reserv():
	form = ReservationForm()
	if form.validate_on_submit():
		reservation = Reservation(
			Room.query.filter_by(room_num=session['room_num']).first(),
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
		room = Room.query.filter_by(room_num = session['room_num']).first()
		room.book_from = form.date_in.data
		room.book_release = form.date_out.data
		# msg = Message("Send Mail Tutorial!",
		# 	sender="magnetreservations@gmail.com",
		# 	recipients=["magnetreservations@gmail.com"])
		# msg.body = "Yo!\nHave you heard the good word of Python???"           
		# mail.send(msg)
		db.session.commit()

		db.session.add(reservation)
		db.session.commit()

		return redirect('/reserve_guest')
	return render_template('reservation/reserv.html', form = form)

	
@app.route('/reserve_guest')
def reserve_guest():
	return "All done"




@app.route("/index")
@login_required
def index():
	#show Guest has not check in and today is the check in day
	result1 = Reservation.query.filter(Reservation.check_in == False).filter_by(date_in = date.today()).all()
	#show guests that check out day is today
	result2 = Reservation.query.filter(Reservation.check_out == False).filter_by(date_out = date.today()).all()
	#current Guests
	curr_result = Reservation.query.filter(Reservation.check_in == True).filter_by(date_in = date.today()).all()

	return render_template('index.html', result1 = result1, result2 = result2, curr_result = curr_result)



@app.route('/check_in/<int:reservation_id>')
@login_required
def check_in(reservation_id):
	reservation = Reservation.query.filter_by(reservation_id = reservation_id).first()
	reservation.check_in = True
	reservation.check_out = False
	db.session.commit()
	flash('guest checked in')
	return redirect('index')



@app.route('/check_out/<int:reservation_id>')
@login_required
def check_out(reservation_id):
	reservation = Reservation.query.filter_by(reservation_id = reservation_id).first()
	reservation.check_out = True
	db.session.commit()
	flash('guest checked out')
	return redirect(url_for('billing', reservation_id=reservation_id))




@app.route('/billing/<int:reservation_id>')
@login_required
def billing(reservation_id):
	result = Reservation.query.filter_by(reservation_id = reservation_id)
	result2 = Room.query.filter(Room.room_num == Reservation.room_num)
	return render_template('reservation/billing.html', result = result, result2 = result2)





