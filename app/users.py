from app.routes import app, db, bcrypt, login_manager
from datetime import datetime
from flask_login import UserMixin
@login_manager.user_loader
def load_user(id):
	return Users.query.get(int(id))

class Users(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(200), nullable=False)
	email = db.Column(db.String(200), nullable=False)
	password = db.Column(db.String(200), nullable=False)
	date_created = db.Column(db.DateTime, default=datetime.now())

	def set_password(self, password):
		self.password = bcrypt.generate_password_hash(password).decode('UTF-8')

	def check_password(self, password):
		return bcrypt.check_password_hash(self.password, password)
	def __repr__(self):
		return f"User('{self.username}', '{self.email}', '{self.id}')"

class Light(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	on = db.Column(db.Boolean, nullable=False)
	date_updated = db.Column(db.DateTime, nullable=False, default=datetime.now())
	user_id_updated = db.Column(db.Integer, nullable=False)
	def update_date(self):
		self.date_updated = datetime.now()

	def light_switch(self):
		self.on = not self.on

	def light_switch(self):
		return self.on
	def __repr__(self):
		return f"Light('{self.id}', '{self.on}', '{self.date_updated}')"