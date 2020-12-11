from flask import Blueprint, Flask, render_template, url_for, request, redirect
import json, os, psycopg2, requests
from ..models.users import currentUser, filterByEmail, registerUser, loginUser, logout_user, filterPlantByID, movePlant, getCurrentUser, filterPlantBySerial
from ..models import redisCon
mod_auth = Blueprint('auth', __name__, url_prefix='/')
weatherapikey= "6545ce0d4b8726f11fee3867ee16ebf8"
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
		outside = True if request.form.get("outside") else False
		#print(username, email, passw)
		print(name, email, passw, number, zip, serial, outside)
		registerUser(name, email, passw, number, zip, serial, outside)
		userid = filterByEmail(email).get_id()
		redisCon.insert(str(userid), str(serial))
		return redirect(url_for('auth.login'))
	else:
		if currentUser():
			return redirect(url_for('auth.index'))
		else:
			return render_template('register.html')

@mod_auth.route('/move', methods=['POST'])
def move():
	id = request.args.get('id')
	plant = filterPlantByID(id)
	print(plant)
	movePlant(plant)
	return redirect(url_for("auth.index"))

@mod_auth.route('/', methods=['POST', 'GET'])
def index():
	if currentUser():
		serial = redisCon.get(str(getCurrentUser().get_id())).decode("utf-8")
		plant= filterPlantBySerial(serial)

		if not plant.outside:
			water = plant.dry
		else:
			rain = rainToday(getCurrentUser().zipcode)
			water = plant.dry and not rain
		return render_template('loggedin.html',
		                       planttype="pottedplant.png" if plant.current_state() else "pottedplant.png" ,
		                       water = water,
		                       user=getCurrentUser().name,
		                       outdoors= "True" if plant.current_state() else "False",
		                       plantid=plant.id)
	else:
		return redirect(url_for("auth.login"))

def rainToday(zip):
	url = "http://api.openweathermap.org/data/2.5/weather?zip={},us&appid={}".format(zip, weatherapikey)
	response = requests.get(url)
	data = response.json()
	lon = data['coord']['lon']
	lat = data['coord']['lat']
	url = "https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude={}&appid={}".format(lat, lon, "current,daily,minutely,alerts", weatherapikey)
	response = requests.get(url)
	data = response.json()
	#print(len(data["hourly"]))
	hourlydata = data["hourly"][:12]
	for i in hourlydata:
		#print(i)
		for j in i["weather"]:
			if j["main"].lower() == "rain":
				return True
	return False
