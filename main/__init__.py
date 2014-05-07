from flask import Blueprint
from flask import Flask
from flask.ext.login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from momentjs import momentjs
from config import ADMINS, MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD
import os
from flask.ext.mail import Mail

basedir = os.path.abspath(os.path.dirname(__file__))
mainapp = Blueprint('main', __name__, template_folder='templates')


app = Flask(__name__)
app.config.from_object('config')
app.jinja_env.globals['momentjs'] = momentjs
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "/login"

#from main.models import User
#from main.models import post_cat
#from main.models import Post
#from main.models import Category
mail = Mail(app)
from main import models
from main import views


#if not app.debug:
#    import logging
#    from logging.handlers import SMTPHandler
#    credentials = None
#    if MAIL_USERNAME or MAIL_PASSWORD:
#        credentials = (MAIL_USERNAME, MAIL_PASSWORD)
#    mail_handler = SMTPHandler((MAIL_SERVER, MAIL_PORT), 'no-reply@' + MAIL_SERVER, ADMINS, 'blog failure', credentials)
#    mail_handler.setLevel(logging.ERROR)
#    app.logger.addHandler(mail_handler)

if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('tmp/microblog.log', 'a', 1 * 1024 * 1024, 10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('blog startup')



