from flask import Blueprint
from flask import Flask
from flask.ext.login import LoginManager
from flask.ext.security import Security, SQLAlchemyUserDatastore
from flask_sqlalchemy import SQLAlchemy
from momentjs import momentjs
from config import ADMINS, MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD
import os
from flask.ext.mail import Mail
from flask.ext.admin import Admin
from flask.ext.restful import Api, Resource
from flask_redis import Redis
#from celery import Celery

basedir = os.path.abspath(os.path.dirname(__file__))
mainapp = Blueprint('main', __name__, template_folder='templates')


app = Flask(__name__)
app.config.from_object('config')
app.jinja_env.globals['momentjs'] = momentjs
db = SQLAlchemy(app)
mail = Mail(app)
redis_store = Redis(app)
from main.models import User
from main.models import Role


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "/login"

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

from main import models
from main import views




