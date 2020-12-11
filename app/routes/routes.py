from flask import Blueprint, Flask, render_template, url_for, request, redirect
import json, os, psycopg2
from ..models.users import currentUser, filterByEmail, registerUser, loginUser, logout_user, filterPlantByID, movePlant, getCurrentUser, filterPlantBySerial
from ..models import redisCon
mod_auth = Blueprint('auth', __name__, url_prefix='/')
@mod_auth.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		if currentUser():
			#print(current_user)
			return redirect(url_for('auth.index'))

		else:
			email = request.form['email']
			passw = request.form['pass']
			user = filterByEmail(email)
			print(user)
			if user is not None and user.check_password(passw):
				print("Here")
				loginUser(user, remember=True)
				print("login")
				return redirect(url_for('auth.index'))
			else:
				return 'Error'
	else:
		if currentUser():
			return redirect(url_for('auth.index'))
		else:
			return render_template('login.html')

@mod_auth.route('/logout')
def logout():
	if currentUser():
		logout_user()
	return redirect(url_for('auth.index'))

# @mod_auth.route('/fun')
# def fun():
# 	redisCon.insert("bob","sucks")
# 	print(redisCon.get("bob"))
# 	return "Hello"

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
		print(name, email, passw, number, zip, serial)
		registerUser(name, email, passw, number, zip)
		userid = filterByEmail(email).get_id()
		redisCon.insert(str(userid), str(serial))
		return redirect(url_for('auth.login'))
	else:
		if currentUser():
			return redirect(url_for('auth.index'))
		else:
			return render_template('register.html')

@mod_auth.route('/move', methods=['POST'])
def match():
	id = request.args.get('id')
	plant = filterPlantByID(id)
	movePlant(plant)
	return id

@mod_auth.route('/', methods=['POST', 'GET'])
def index():
	if currentUser():
		serial = redisCon.get(str(getCurrentUser().get_id())).decode("utf-8")
		plant= filterPlantBySerial(serial)
		return render_template('loggedin.html',
		                       planttype="pottedplant.png",
		                       user="current_user.username",
		                       indoors= "True" if plant.current_state() else "False",
		                       plantid="plant.id")
	else:
		return redirect(url_for("auth.login"))
