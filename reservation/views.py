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
from flask.ext.mail import Mail, Message
#this is forf the aws
application = Flask(__name__)


# sending mail testing
# @app.route('/send_mail')
# def send_mail(to):
#     msg = Message(
#     	'Hello',
#     	sender='magnetreservations@gmail.com',
#     	recipients=[to])
#     msg.body = "This is the email body"
#     msg.html = render_template('reservation/invoice/<int:reservation_id>.html')
#     mail.send(msg)


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
		third_check = Room.query.filter(Room.book_release > search.date_in).count()
		count_Rooms = Room.query.count()

		#if date is not correct or the date in is past (for example the input date in yesterday)
		if form.date_in.data >= form.date_out.data or form.date_in.data < date.today():
			flash ("Please enter a valid date")

		#if all the rooms are avalible	
		elif first_check:
			result_sta = Room.query.filter_by(status=True).order_by(Room.room_num.desc())
			return render_template('reservation/result.html', result = result_sta)

		# if there are no rooms availble
		elif third_check >=count_Rooms:
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

		first_name = form.first_name.data
		last_name = form.last_name.data
		date_in = form.date_out.data
		date_out = form.date_out.data
		##confirmation email
		msg = Message('Magnet Reservation',
			sender='magnetreservations@gmail.com',
			recipients=[form.email.data])
		msg.body = "This is the email body"
		msg.html = render_template('reservation/booking_confirm.html', first_name = first_name, last_name=last_name,
			date_in=date_in,date_out=date_out)
		mail.send(msg)
		db.session.commit()

		db.session.add(reservation)
		db.session.commit()

		return redirect('/res_confirm')
	return render_template('reservation/reserv.html', form = form)



@app.route('/res_confirm')
def reserve_guest():
	return render_template('reservation/res_confirm.html')




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

	return redirect(url_for('invoice', reservation_id=reservation_id))




@app.route('/invoice/<int:reservation_id>')
@login_required
def invoice(reservation_id):
	result = Reservation.query.filter_by(reservation_id = reservation_id)
	result2 = Room.query.filter(Room.room_num == Reservation.room_num)
	for reservation in result:
		for room in result2:
			if reservation.room_num == room.room_num:
				msg = Message(
					'Magnet Reservation Invoice',
					sender='magnetreservations@gmail.com',
					recipients=[reservation.email])
				msg.body = "This is the email body"
				msg.html = render_template('reservation/invoice.html',result = result, result2 = result2, created=date.today())
				mail.send(msg)

	return render_template('reservation/invoice.html', result = result, result2 = result2, created=date.today())





