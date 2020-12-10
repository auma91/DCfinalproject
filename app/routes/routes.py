from flask import Blueprint, Flask, render_template, url_for, request, redirect
import json, os, psycopg2
from ..models.users import currentUser, filterByEmail, registerUser, loginUser, logout_user

mod_auth = Blueprint('auth', __name__, url_prefix='/')
# @app.route('/login', methods=['GET', 'POST'])
# def login():
# 	print("Hello")
# 	if request.method == 'POST':
# 		if currentUser():
# 			#print(current_user)
# 			return redirect(url_for('/'))
#
# 		else:
# 			email = request.form['email']
# 			passw = request.form['pass']
# 			user = filterByEmail(email)
# 			if user is not None and user.check_password(passw):
# 				loginUser(user, remember=True)
# 				next_page = request.args.get('next')
# 				#print(next_page)
# 				if next_page is None:
# 					next_page = url_for('/')
# 				#print(next_page)
# 				return redirect(next_page)
# 			else:
# 				return 'Error'
# 	else:
# 		if currentUser():
# 			return redirect(url_for('/'))
# 		else:
# 			return render_template('login.html')
#
# @app.route('/logout')
# def logout():
# 	logout_user()
# 	return redirect(url_for('index'))
#
# @app.route('/register', methods=['GET', 'POST'])
# def register():
# 	if request.method == 'POST':
# 		if currentUser():
# 			return redirect(url_for('index'))
# 		username = request.form['username']
# 		email = request.form['email']
# 		passw = request.form['pass']
# 		#print(username, email, passw)
# 		registerUser(username, email, passw)
# 		return redirect(url_for('login'))
# 	else:
# 		if currentUser():
# 			return redirect(url_for('index'))
# 		else:
# 			return render_template('register.html')

@mod_auth.route('/', methods=['POST', 'GET'])
def index():
	print("Work")
	return render_template('loggedin.html', user="current_user.username", light="ON")

