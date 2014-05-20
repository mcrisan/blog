from flask import Blueprint
from flask import Flask
from flask.ext.login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from momentjs import momentjs
from config import ADMINS, MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD
import os
from flask.ext.mail import Mail
from flask.ext.admin import Admin

#from blog.admin import MyView
#from blog.admin.views import MyView
#from blog import MyView 
basedir = os.path.abspath(os.path.dirname(__file__))
mainapp = Blueprint('main', __name__, template_folder='templates')


app = Flask(__name__)
app.config.from_object('config')
app.jinja_env.globals['momentjs'] = momentjs
db = SQLAlchemy(app)
mail = Mail(app)
from blog.admin import PostView, TagsView, CategoriesView, CommentsView
from user.admin import UserView
from flask.ext.admin.contrib.sqla import ModelView
from main.models import User, Tags, Category
admin = Admin(app)
#admin.add_view(MyView())
#admin.add_view(ModelView(User, db.session))
admin.add_view(UserView(db.session))
admin.add_view(PostView(db.session, endpoint="postview"))
admin.add_view(TagsView(db.session))
admin.add_view(CategoriesView(db.session))
admin.add_view(CommentsView(db.session))
#admin.add_view(ModelView(Category, db.session))


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "/login"

#from main.models import User
#from main.models import post_cat
#from main.models import Post
#from main.models import Category

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



