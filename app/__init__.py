from flask import Flask
from app import routes, models
def create_app():
	app = Flask(__name__)
	##################################
	# config
	DB_URL = "postgres+psycopg2://postgres:9I4ME8ghDvrBorou@35.232.202.135:5432/irrigation"
	# os.environ.get("DATABASE_URL")[0:8] + '+psycopg2' + os.environ.get("DATABASE_URL")[8::]
	app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
	app.config['SECRET_KEY'] = 'you-will-never-guess'
	models.init_app(app)
	from app.routes.routes import mod_auth as auth_module

	# Register blueprint(s)
	app.register_blueprint(auth_module)
	# login_manager.login_message_category = 'info'
	####################################
	return app