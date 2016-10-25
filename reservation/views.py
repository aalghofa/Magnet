# Display reservation view for guest
# Yousef Alahrbi
# 10/19/2016


# add libraries
from Magnet import app, db
from flask import render_template, redirect, session, request, url_for, flash
from reservation.form import SearchForm, ReservationForm, AddRoomForm
from reservation.models import Search, Reservation, Room

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
	result = Room.query.filter_by(status = True)
	return render_template('reservation/result.html', result = result)

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
			members=form.members.data,
			email=form.email.data,
			phone_num=form.phone_num.data,
			address=form.address.data,
			city=form.city.data,
			state=form.state.data,
			zip_code=form.zip_code.data,

			)
		db.session.add(reservation)
		db.session.commit()


		
		# db.session.commit()
		return redirect('/reserve_guest')
	return render_template('reservation/reserv.html', form = form)

	
@app.route('/reserve_guest')
def reserve_guest():
	# author = Author.query.filter_by(username=session['username']).first()
	# reservation = Reservation.query.filter_by(last_name=session['last_name'])
	# reserved = Reserved(reservation)
	# db.session.add(reserved)
	# db.session.commit()
	return "All done"



@app.route("/index")
def index():
	return "Hello World"









