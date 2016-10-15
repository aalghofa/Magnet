
    #database set for the employee
    
    
    ##############################################
    # Current Plan is to have Admin added by directly interacting with mysql
    # and Receptionist can be added by the Admin filling out a form within the Receptionist's info
    ##############################################
from Magnet import db
    
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(80))
    email = db.Column(db.String(35), unique=True)
    job_title = db.Column(db.String(20))
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(60))
    
    is_admin = db.Column(db.Boolean) #boolean: if true then admin if false then Receptionist, false by defalut(in case of admin need to be created var can be override)
    #posts = db.relationship('Post', backref='employee', lazy='dynamic')
    
    def __init__(self, fullname, email, job_title, username, password, is_admin=False):
        self.fullname = fullname
        self.email = email
        self.job_title = job_title
        self.username = username
        self.password = password
        self.is_admin = is_admin
    # repr allows to interact witht the db from the terminal by calling it Employee and by its username
    def __repr__(self):
        return '<Employee %r>' % self.username
