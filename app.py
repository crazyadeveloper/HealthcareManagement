from flask import Flask, Markup, render_template, flash, redirect, url_for, session, request, logging
from flask_mysqldb import MySQL
from wtforms import Form, IntegerField, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps

app = Flask(__name__)
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
		#flash('You are now registered and can log in', 'success')
		return redirect(url_for('plog'))
	return render_template('patient_signup.html', form = form)

@app.route('/dsign', methods=['GET', 'POST'])
def dsign():
	form = DRegisterForm(request.form)
	if(request.method == 'POST' and form.validate()):
		name = form.name.data 
		email = form.email.data 
		username = form.username.data 
		phone = form.phone.data 
		address = form.address.data 
		spec = form.spec.data 
		fee = form.fee.data 
		password = form.password.data

		cur = mysql.connection.cursor()
		result = cur.execute("SELECT * FROM doctors WHERE doc_username = %s", [username])
		if result > 0:
			error = 'Username found'
			return render_template('dr_signup.html', error = error, form = form)
		result = cur.execute("SELECT * FROM doctors WHERE doc_email = %s", [email])
		if result > 0:
			error = 'email found'
			return render_template('dr_signup.html', error = error, form = form)


		cur.execute("INSERT INTO doctors(doctor_name ,doctor_spec ,doc_mobileNo ,doc_email ,doc_password ,doc_address ,doc_username ,doc_fees ) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)", (name, spec, phone, email, password, address, username, fee))
		mysql.connection.commit()
		cur.close()

		#FLASH IS NOT WORKING
		#flash('You are now registered and can log in', 'success')
		return redirect(url_for('dlog'))
	return render_template('dr_signup.html', form=form)


@app.route('/plog', methods=['GET', 'POST'])
def plog():
	form = LoginForm(request.form)
	if(request.method == 'POST' and form.validate()):
		username = form.username.data
		password = form.password.data
		cur = mysql.connection.cursor()
		result = cur.execute("SELECT * FROM patients WHERE patient_username = %s AND patient_password = %s", [username, password])
		if result == 1:
			return redirect(url_for('user', username=username))
		else:
			error = 'Username/Password Incorrect'
			return render_template('patient_login.html', error = error, form = form)
	return render_template('patient_login.html', form = form)

@app.route('/dlog', methods=['GET', 'POST'])
def dlog():
	form = LoginForm(request.form)
	if(request.method == 'POST' and form.validate()):
		username = form.username.data
		password = form.password.data
		cur = mysql.connection.cursor()
		result = cur.execute("SELECT * FROM doctors WHERE doc_username = %s AND doc_password = %s", [username, password])
		if result == 1:
			return redirect(url_for('userd', username=username))
		else:
			error = 'Username/Password Incorrect'
			return render_template('dr_login.html', error = error, form = form)
	return render_template('dr_login.html', form = form)


@app.route('/user/<username>', methods=['GET', 'POST'])
def user(username):
	return render_template('pdashboard.html', un=username)

@app.route('/userd/<username>', methods=['GET', 'POST'])
def userd(username):
	return render_template('ddashboard.html', un=username)
@app.route('/makeappt/<username>',methods=['GET', 'POST'])
def makeappt(username):
	cursor = mysql.connection.cursor()
	cur = cursor.execute("SELECT doctor_spec FROM doctors")
	ars = cursor.fetchall()
	cursr = mysql.connection.cursor()
	fact = cursr.execute("SELECT doc_username , doctor_name , doc_address ,doc_fees FROM doctors" )
	dt = cursr.fetchall()
	if request.method == "POST":
		word = request.form.get("spec", None)
		if word!=None:
			return render_template('appt_pt.html', tot=ars ,total=dt , word= word)
	return render_template('appt_pt.html', tot=ars , total = dt)

@app.route('/apptListdr/<username>', methods=['GET', 'POST'])
def apptListdr(username):
	cur = mysql.connection.cursor()
	res2 = cur.execute("SELECT a.patient_id, p.patient_name, a.date, a.time  FROM appointments a, patients p, doctors d WHERE a.patient_id = p.patient_id AND d.doctor_id = a.doctor_id AND d.doc_username = %s", [username])
	rv = cur.fetchall()
	return render_template('appt_dr.html', data=rv)

if __name__ == '__main__':
	app.secret_key='secret123'
	app.run(debug=True)
