from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import redis
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'login'
redisConnection = None
def init_app(app, host):
	global redisConnection
	db.init_app(app)
	login_manager.init_app(app)
	bcrypt.init_app(app)
	redisConnection = redis.Redis(
		host=host,
		port=6379)