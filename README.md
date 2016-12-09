# Project Name: MAGNET - Hotel Management System - Web Based Application
# Project Version: 1.0
# Devolpers: Abdullah Alghofaili & Yousef Alharbi
# Course Name: Capstone Project
# Semester: Fall 2016
### This file demonstrates steps to run MAGNET.
### link to the application website: aalghofa.pythonanywhere.com

# Compiling steps:
 *     Note: before you run the application, make sure you have python 3 installed on your machine. *
 
1. Clone MAGNET repository or download the zip file
2. Create a database using mysql
3. Edit _settings.py_ file to configure your database:
	- Update _DB_USERNAME_ to your database username.
	- Update _DB_PASSWORD_ to your databse password.
4. delete the **venv** directory if exists
5. create a new virtual environment by typing this command:
    ~~~~ 
    virtualenv -p python3 venv
    ~~~~
6. activate your virtual environment by typing this command:
   ~~~~ 
   source venv/bin/activate
   ~~~~
7. install the packages requirements:
   ~~~~ 
   pip install -r requirements.txt
   ~~~~
8. run the application by typing this command: 
   ~~~~ 
   python _manage.py_ runserver
   ~~~~
9. After you run the command in step 8, open manage.py file and comment the creation of your database. Comment the following lines in manage.py:
	~~~~
	from employee.models import *
	from reservation.models import *
	db.create_all()
	~~~~
You need to create your database only once, therefore once you created it you do not need to create it again.

10. Open web browser and type your localhost address as url link, you should see the application running.

