
from main import mainapp
from main import app
from blog import blog
from user import users
from admin import admin
from service import service


app.register_blueprint(mainapp, url_prefix='')
app.register_blueprint(blog, url_prefix='')
app.register_blueprint(users, url_prefix='')
app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(service, url_prefix='/service')


app.run(debug=True)