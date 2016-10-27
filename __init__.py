from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import flask_whooshalchemy

app = Flask(__name__)
app.config.from_object('settings')
db = SQLAlchemy(app)

# migrations
migrate = Migrate(app, db)


app.config['WHOOSH_BASE'] = 'whoosh'

from reservation import views
from employee import views


