from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail

app = Flask(__name__)
app.config.from_object('settings')
db = SQLAlchemy(app)

# migrations
migrate = Migrate(app, db)

#mail
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'magnetreservations@gmail.com'
app.config['MAIL_PASSWORD'] = 'Magnet123;'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

from reservation import views
from employee import views


