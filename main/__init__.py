from flask import Blueprint
from flask import Flask
from flask.ext.login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from momentjs import momentjs
from config import ADMINS, MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD
import os
from flask.ext.mail import Mail
from flask.ext.admin import Admin
from flask.ext.restful import Api, Resource


basedir = os.path.abspath(os.path.dirname(__file__))
mainapp = Blueprint('main', __name__, template_folder='templates')


app = Flask(__name__)
app.config.from_object('config')
app.jinja_env.globals['momentjs'] = momentjs
db = SQLAlchemy(app)
mail = Mail(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "/login"



from main import models
from main import views




