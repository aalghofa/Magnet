from Magnet import app, db
from flask import render_template, redirect, session, request, url_for, flash
from employee.form import RegisterForm, LoginForm
from employee.models import Employee
from employee.decorators import login_required, admin_required
import bcrypt
from flask_table import Table, Col

@app.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    error = None

    if request.method == 'GET' and request.args.get('next'):
        session['next'] = request.args.get('next', None)

    if form.validate_on_submit():
        employee = Employee.query.filter_by(
        	live=True,
            username=form.username.data,
            ).first()
        if employee:
            if bcrypt.hashpw(form.password.data, employee.password) == employee.password:
                session['username'] = form.username.data
                session['is_admin'] = employee.is_admin
                if 'next' in session:
                    next = session.get('next')
                    session.pop('next')
                    return redirect(next)
                else:
                    return redirect('index')
            else:
                error = "Incorrect password"
        else:
            error = "employee not found"
    return render_template('employee/login.html', form=form, error=error)

@app.route('/register', methods=('GET', 'POST'))
#admin is required to fill the form in order to add a Receptionist
@admin_required
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(form.password.data, salt)
        employee = Employee(
            form.fullname.data,
            form.email.data,
            form.job_title.data,
            form.username.data,
            hashed_password,
            False,
            True
        )
        db.session.add(employee)
        db.session.commit()

        return redirect('/success')
    return render_template('employee/register.html', form=form)

##########################list of employees #####################
@app.route('/admin')
@login_required
@admin_required
def admin():
    #posts = Employee.query.order_by(Employee.id.desc())
    posts = Employee.query.filter_by(live=True).order_by(Employee.id.desc())
    return render_template('employee/admin.html', posts=posts)

@app.route('/success')
@login_required
def success():
    return "employee registered!"


@app.route('/delete/<int:employee_id>')
@admin_required
def delete(employee_id):
    employee = Employee.query.filter_by(id=employee_id).first_or_404()
    employee.live = False
    db.session.commit()
    flash("Employee deleted")
    return redirect('/admin')



# @app.route('/ItemTable')
# # Declare your table
# class ItemTable(Table):
#     fullname = Col('Name')
#     username = Col('username')

# # Get some objects
# class Item(object):
#     def __init__(self, fullname, username):
#         self.fullname = fullname
#         self.username = username
# items = Employee.query.all()

# # Populate the table
# table = ItemTable(items)

# # Print the html
# print(table.__html__())
