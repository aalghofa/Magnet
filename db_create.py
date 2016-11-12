from Magnet import db
from employee.models import *
from reservation.models import *

db.create_all()

print("DB created.")