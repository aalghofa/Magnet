# This is a flask web based app. A hotel management and reservation system.
# Part of kent state capstone class Fall 2016
# developed by Abdullah Alghofaili and Yousef Alharbi.


#next two lines basiclly works as apointer to tell python where the starting point of the app is
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask_script import Manager, Server
from flask_migrate import MigrateCommand
from Magnet import app

##### the following 3 lines to create the database for the first time.
from employee.models import *
from reservation.models import *
db.create_all()
######
manager = Manager(app)
manager.add_command('db', MigrateCommand)

manager.add_command("runserver", Server(
	use_debugger = True,
	use_reloader = True,
	host = os.getenv('IP', '127.0.0.1'),
	port = int(os.getenv('PORT', 5000))
	)
)


if __name__ == "__main__":
	manager.run()
