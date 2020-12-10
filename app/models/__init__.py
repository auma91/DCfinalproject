from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'login'

def init_app(app):
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)