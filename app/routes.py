from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, current_user, logout_user, login_required
from flask_bcrypt import Bcrypt
import json, os, psycopg2
from app.users import load_user, Users,Light
###################################
#config
app = Flask(__name__)
DB_URL = "postgres+psycopg2://spssvllasvujqp:63a948723ae021da3156d22b0259fdbaa0979dc77977b092059c528968393349@ec2-52-44-55-63.compute-1.amazonaws.com:5432/d4ginmtjpblc2s"
#os.environ.get("DATABASE_URL")[0:8] + '+psycopg2' + os.environ.get("DATABASE_URL")[8::]
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SECRET_KEY'] = 'you-will-never-guess'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
# login_manager.login_message_category = 'info'
####################################


@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		if current_user.is_authenticated:
			#print(current_user)
			return redirect(url_for('/'))

		else:
			email = request.form['email']
			passw = request.form['pass']
			user = Users.query.filter_by(email=email).first()
			if user is not None and user.check_password(passw):
				login_user(user, remember=True)
				next_page = request.args.get('next')
				#print(next_page)
				if next_page is None:
					next_page = url_for('/')
				#print(next_page)
				return redirect(next_page)
			else:
				return 'Error'
	else:
		if current_user.is_authenticated:
			return redirect(url_for('/'))
		else:
			return render_template('login.html')

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
	if request.method == 'POST':
		if current_user.is_authenticated:
			return redirect(url_for('index'))
		username = request.form['username']
		email = request.form['email']
		passw = request.form['pass']
		#print(username, email, passw)
		user = Users(username=username, email=email)
		user.set_password(passw)
		db.session.add(user)
		db.session.commit()
		return redirect(url_for('login'))
	else:
		if current_user.is_authenticated:
			return redirect(url_for('index'))
		else:
			return render_template('register.html')
