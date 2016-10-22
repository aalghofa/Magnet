# Display reservation view for guest
# Yousef Alahrbi
# 10/19/2016


# add libraries
from Magnet import app, db
from flask import render_template, redirect, session, request, url_for, flash
from reservation.form import SearchForm, ReservationForm, AddRoomForm
from reservation.models import Search, Reservation, Room, reserved

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
		db.session.add(search)
		db.session.commit()
		return redirect('/results')
	return render_template('reservation/search.html', form = form)
	
@app.route('/results', methods=('GET', 'POST'))
def results():
	result = Room.query.filter_by(status = False)
	return render_template('reservation/result.html', result = result)

@app.route('/book/<int:room_id>')
def book(room_id):
    room = Room.query.filter_by(id=room_id).first_or_404()
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
			form.zip_code.data
			)
		db.session.add(reservation)
		db.session.commit()

		#x = Room.query.filter_by(Room.reserved.any(room_id=room_id))
		
		return redirect('/reserve_guest')
	return render_template('reservation/reserv.html', form = form)

	
@app.route('/reserve_guest')
def reserve_guest():
	return "All done"



@app.route("/index")
def index():
	return "Hello World"









