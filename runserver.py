from flask.ext.restful import Api
from flask.ext.admin import Admin

from main import mainapp
from main import app,db
from blog import blog
from blog.admin import PostView, TagsView, CategoriesView, CommentsView
from user import users
from user.admin import UserView
from service import service
from service.restful_service import UserAPI, UsersListAPI, PostAPI, TokenAPI

app.register_blueprint(mainapp, url_prefix='')
app.register_blueprint(blog, url_prefix='')
app.register_blueprint(users, url_prefix='')
app.register_blueprint(service, url_prefix='/service')


admin = Admin(app)
admin.add_view(UserView(db.session))
admin.add_view(PostView(db.session, endpoint="postview"))
admin.add_view(TagsView(db.session))
admin.add_view(CategoriesView(db.session))
admin.add_view(CommentsView(db.session))

api = Api(app)
api.add_resource(UserAPI, '/api/user/<int:id>', endpoint = 'user')
api.add_resource(TokenAPI, '/api/token', endpoint = 'token')
api.add_resource(UsersListAPI, '/api/users', endpoint = 'userlists')
api.add_resource(PostAPI, '/api/post/<int:id>', endpoint = 'post')


if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('tmp/microblog.log', 'a', 1 * 1024 * 1024, 10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('blog startup')

app.run(debug=True)