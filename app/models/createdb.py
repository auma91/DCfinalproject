from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import UserMixin
from datetime import datetime
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres+psycopg2://postgres:9I4ME8ghDvrBorou@35.232.202.135:5432/irrigation'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class Users(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(200), nullable=False)
	email = db.Column(db.String(200), nullable=False)
	password = db.Column(db.String(200), nullable=False)
	phone = db.Column(db.String(20), nullable=True)
	zipcode = db.Column(db.Integer, nullable=False)
	date_created = db.Column(db.DateTime, default=datetime.now())

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
	def update_state(self):
		self.outside = not self.outside
	def current_state(self):
		return self.on
	def __repr__(self):
		return f"Light('{self.id}', '{self.outside}', '{self.serial}')"

db.create_all()
db.session.commit()