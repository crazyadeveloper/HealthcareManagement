from flask import Flask, Markup, render_template, flash, redirect, url_for, session, request, logging
from flask_mysqldb import MySQL
from wtforms import Form, IntegerField, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
from flask_mail import Mail, Message
from wtforms.fields.html5 import DateField
from datetime import date
from wtforms.validators import DataRequired
#import smtplib
import random

app = Flask(__name__)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'xyz@gmail.com'
app.config['MAIL_PASSWORD'] = 'xyz'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
posta = Mail(app)
#app.secret_key = "super secret key"


app.config['MYSQL_HOST'] = 'remotemysql.com'
app.config['MYSQL_USER'] = 'k74YQgoO0D'
app.config['MYSQL_PASSWORD'] = 'iWAowcfHMK'
app.config['MYSQL_DB'] = 'k74YQgoO0D'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/')
def index():
	return render_template("homepage.html")

class RegisterForm(Form):
    name = StringField('Name*', [validators.DataRequired(),validators.Length(min=1, max=50)])
    address = StringField('Address', [validators.optional(), validators.length(min=1, max=50)])
    phone = IntegerField('Phone No*', [validators.DataRequired()])
    email = StringField('Email*', [validators.DataRequired(),validators.Length(min=6, max=50), validators.Email()])
    username = StringField('Username*', [validators.DataRequired(),validators.Length(min=4, max=25)])
    sex = StringField('Gender*', [validators.DataRequired(),validators.Length(min=4, max=6)])
    blood = StringField('Blood Group', [validators.optional(), validators.Length(min=2, max=4)])
    age = StringField('Age', [validators.optional()])
    password = PasswordField('Password*', [
        validators.DataRequired(), validators.Length(min=4, max=16),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password*')

class DRegisterForm(Form):
    name = StringField('Name*', [validators.DataRequired(),validators.Length(min=1, max=50)])
    spec = StringField('Field of Specialization*', [validators.DataRequired(),validators.Length(min=1, max=20)])
    address = StringField('Chamber Address*', [validators.DataRequired(),validators.length(min=1, max=50)])
    phone = IntegerField('Phone No*', [validators.DataRequired()])
    fee = IntegerField('Fees*', [validators.DataRequired()])    
    email = StringField('Email*', [validators.DataRequired(),validators.Length(min=6, max=20), validators.Email()])
    username = StringField('Username*', [validators.DataRequired(),validators.Length(min=4, max=10)])
    password = PasswordField('Password*', [
        validators.DataRequired(), validators.Length(min=4, max=16),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password*')

class LoginForm(Form):
    username = StringField('Username*', [validators.DataRequired(),validators.Length(min=4, max=25)])
    password = PasswordField('Password*', [
        validators.DataRequired(), validators.Length(min=4, max=16)
    ])

class  BookForm(Form) :
	usernae = StringField('Username*', [validators.DataRequired(),validators.Length(min=4, max=25)])
	startdate = DateField("Enter the date for your appointment*", default=date.today(), format='%d/%m/%Y', validators=[DataRequired()],)

@app.route('/psign', methods=['GET', 'POST'])
def psign():
	form = RegisterForm(request.form)
	if(request.method == 'POST' and form.validate()):
		name = form.name.data 
		email = form.email.data 
		username = form.username.data 
		phone = form.phone.data 
		sex = form.sex.data 
		address = form.address.data 
		blood = form.blood.data 
		age = form.age.data 
		password = form.password.data

		cur = mysql.connection.cursor()
		result = cur.execute("SELECT * FROM patients WHERE patient_username = %s", [username])
		if result > 0:
			error = 'Username found'
			return render_template('patient_signup.html', error = error, form = form)
		result = cur.execute("SELECT * FROM patients WHERE patient_email = %s", [email])
		if result > 0:
			error = 'email found'
			return render_template('patient_signup.html', error = error, form = form)

		cur.execute("INSERT INTO patients(patient_name, patient_address, patient_phno, patient_email, patient_username, patient_password, patient_bloodgroup, patient_sex, patient_age) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)", (name, address, phone, email, username, password, blood, sex, age))
		mysql.connection.commit()
		cur.close()

		#FLASH IS NOT WORKING
		#flash('You are now registered and can log in', 'success'
