from flask import Flask
from app import routes, models
def create_app():
	app = Flask(__name__)
	##################################
	# config
	DB_URL = "postgres+psycopg2://spssvllasvujqp:63a948723ae021da3156d22b0259fdbaa0979dc77977b092059c528968393349@ec2-52-44-55-63.compute-1.amazonaws.com:5432/d4ginmtjpblc2s"
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