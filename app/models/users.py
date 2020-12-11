from flask_login import UserMixin, login_user, logout_user, login_required
from datetime import datetime
from flask_login import UserMixin, current_user
from . import db, bcrypt, login_manager

def filterByEmail(email):
	return Users.query.filter_by(email=email).first()

def filterPlantByID(id):
	return Plant.query.filter_by(id=id).first()

def filterPlantBySerial(serial):
	return Plant.query.filter_by(serial=serial).first()

def movePlant(plant):
	plant.update_state()
	db.session.add(plant)
	db.session.commit()

def registerUser(username, email, password, phone, zip, serial, outside):
	print("Here")
	user = Users(name=username, email=email, phone=phone, zipcode=zip)
	plant = Plant(outside=outside, serial=serial, dry=True)
	user.set_password(password)
	db.session.add(user)
	db.session.add(plant)
	db.session.commit()
def currentUser():
	return current_user.is_authenticated

def getCurrentUser():
	return current_user

def loginUser(user, remember=True):
	login_user(user, remember=True)

@login_manager.user_loader
def load_user(id):
	return Users.query.get(int(id))

class Users(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(200), nullable=False)
	email = db.Column(db.String(200), nullable=False)
	password = db.Column(db.String(200), nullable=False)
	phone = db.Column(db.String(20), nullable=True)
	zipcode = db.Column(db.Integer, nullable=False)
	date_created = db.Column(db.DateTime, default=datetime.now())

	def get_id(self):
		return self.id

	def set_password(self, password):
		self.password = bcrypt.generate_password_hash(password).decode('UTF-8')

	def check_password(self, password):
		return bcrypt.check_password_hash(self.password, password)
	def __repr__(self):
		return f"User('{self.name}', '{self.email}', '{self.id}')"

class Plant(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	outside = db.Column(db.Boolean, nullable=False)
	serial = db.Column(db.String(50), nullable=False)
	dry = db.Column(db.Boolean, nullable=False)

	def get_id(self):
		return self.id
	def update_state(self):
		self.outside = not self.outside
	def current_state(self):
		return self.outside
	def isDry(self):
		return self.dry
	def update_dry(self):
		self.dry = not self.dry
	def __repr__(self):
		return f"Light('{self.id}', '{self.outside}', '{self.serial}')"