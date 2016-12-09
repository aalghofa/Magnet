from Magnet import app, db
from flask import render_template, redirect, session, request, url_for, flash
from employee.form import RegisterForm, LoginForm
from employee.models import Employee
from employee.decorators import login_required, admin_required
import bcrypt
# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

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

@app.route("/addEmployees", methods=('GET', 'POST'))
#admin is required to fill the form in order to add a Receptionist
@admin_required
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(form.password.data, salt)
        fullname = form.fullname.data
        ssn = form.ssn.data
        email = form.email.data
        DOB = form.DOB.data
        job_title = form.job_title.data
        username = form.username.data
        password = hashed_password
        if job_title == 'Maneger' or job_title == 'maneger':
            is_admin = True
        else:
            is_admin = False
        live = True
        employee = Employee(fullname,ssn,email,DOB,job_title,username,password,is_admin,live)
        db.session.add(employee)
        db.session.commit()
        flash ("Employee is added")
        return redirect('/addEmployees')
        
    return render_template('addEmployees.html', form=form)



###################### List of employees #############

@app.route('/manageEmployee')
@login_required
@admin_required
def active_emp():
    active = Employee.query.filter_by(live = True).order_by(Employee.id.desc())
    #return redirect(url_for('deactivate',employee_id = Employee.id))
    inactive = Employee.query.filter_by(live=False).order_by(Employee.id.desc())
   # return redirect(url_for('reactivate',employee_id = Employee.id))
    return render_template('manageEmployee.html', active=active, inactive=inactive)


# change employees statuse. if active change to inactive, elseif inactive change it to active
@app.route('/manageEmployee/<int:employee_id>')
@admin_required
def changeStatus(employee_id):
    
    employee = Employee.query.filter_by(id=employee_id).first_or_404()
    liveEmp = employee.live ==True
    NliveEmp = employee.live == False

    if liveEmp:
        employee.live = False
        flash("Employee Deativated")
        db.session.commit()
        return redirect('/manageEmployee')

    elif NliveEmp:
        employee.live = True
        flash("Employee Activated")
        db.session.commit()
        return redirect('/manageEmployee')



@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('is_admin', None)
    return redirect(url_for('login'))

