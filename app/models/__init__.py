from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from .keyvalue import redisConnection
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'login'
redisCon = redisConnection()
def init_app(app, host):
	db.init_app(app)
	login_manager.init_app(app)
	bcrypt.init_app(app)
	redisCon.setConnection(host)