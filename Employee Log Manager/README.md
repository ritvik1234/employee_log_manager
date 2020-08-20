# README #

This README would normally document whatever steps are necessary to get your application up and running.

### What is this repository for? ###
This project is an Employee Log Manager, where users can checkin, checkout daily and check their salary and time logs.
Also, we have an admin, who can create update delete employees, as well as he can check all the time logs of all the users and can also calculate the monthly manpower investment.

* Quick summary
* Version
* [Learn Markdown](https://bitbucket.org/tutorials/markdowndemo)

### How do I get set up? ###

* Summary of set up
* To use this project in your device, you need to firstly clone it in a directory.
* Then in Command prompt : Pip install -r requirements.txt (for the project directory) 
* You can either create a virtual environment or perform it without the virtual environment.
* After installing, Download postgres in your system(if not installed) and in the SQL Shell
Create Database employee; in the postres user.
* After creating an employee, go to the settings.py in elm/elm and in Database, change the password to the one you have chosen while installing postgres or if pre-installed , the password of your postgres user.
* Then, make a migrations folder in elm/api and in that migrations folder, make a __init__.py file.
* Now, Open CMD with elm directory and migrate the models through these commands 
* python manage.py makemigrations and python manage.py migrate
* Now, your models are ready, now run the server : python manage.py runserver
* Then create a super-user which will be the admin for the project 
 python manage.py createsuperuser and add the details.
* Now in the address bar paste : http://127.0.0.1:8000/login/ paste to use the project
* Login with the admin credentials, to create users and can perform different tasks as users.
* To test the password change, you need to make changes in the following variables in settings.py file. You need to have a 2-step authentication of email. 
EMAIL_HOST_USER
EMAIL_HOST_PASSWORD 


### Who do I talk to? ###
*Ritvik Munjal
*Email: 2017meb1234@iitrpr.ac.in
*Mobile no: 7696011532

