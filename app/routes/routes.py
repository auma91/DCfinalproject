from flask import Blueprint, Flask, render_template, url_for, request, redirect
import json, os, psycopg2
from ..models.users import currentUser, filterByEmail, registerUser, loginUser, logout_user
from ..models.keyvalue import insert, get
mod_auth = Blueprint('auth', __name__, url_prefix='/')
@mod_auth.route('/login', methods=['GET', 'POST'])
def login():
	print("Hello")
	if request.method == 'POST':
		if currentUser():
			#print(current_user)
			return redirect(url_for('/'))

		else:
			email = request.form['email']
			passw = request.form['pass']
			user = filterByEmail(email)
			if user is not None and user.check_password(passw):
				loginUser(user, remember=True)
				next_page = request.args.get('next')
				#print(next_page)
				if next_page is None:
					next_page = url_for('/')
				#print(next_page)
				return redirect(next_page)
			else:
				return 'Error'
	else:
		if currentUser():
			return redirect(url_for('/'))
		else:
			return render_template('login.html')

@mod_auth.route('/logout')
def logout():
	if currentUser():
		logout_user()
	return redirect(url_for('auth.index'))

@mod_auth.route('/fun')
def fun():
	insert("bob","sucks")
	print(get("bob"))
	return "Hello"

@mod_auth.route('/register', methods=['GET', 'POST'])
def register():
	if request.method == 'POST':
		if currentUser():
			return redirect(url_for('index'))
		name = request.form['name']
		email = request.form['email']
		passw = request.form['pass']
		number = request.form['phone']
		zip = request.form['zip']
		serial = request.form['serial']

		#print(username, email, passw)
		registerUser(name, email, passw)
		return redirect(url_for('auth.login'))
	else:
		if currentUser():
			return redirect(url_for('auth.index'))
		else:
			return render_template('register.html')

@mod_auth.route('/', methods=['POST', 'GET'])
def index():
	print("Work")
	return render_template('loggedin.html', user="current_user.username", light="ON")

