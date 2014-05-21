from flask.ext.restful import Resource, reqparse, abort, fields, marshal, marshal_with
from main.models import User, Post
from main import db


comment_fields = {
    'comment': fields.String,
    'created_at': fields.String,
    'likes': fields.Integer,
    'unlikes': fields.Integer
}

post_fields = {
    'title': fields.String,
    'excerpt': fields.String,
    'status': fields.Integer,
    'created_at': fields.String,
    'username' : fields.String,
    'test' : fields.String
}

user_fields = {
    'username': fields.String,
    'email': fields.String,
    'type': fields.Boolean,
    'uri': fields.Url('user', absolute=True),
    'comments': fields.Nested(comment_fields)
}

#parser = reqparse.RequestParser()
#parser.add_argument('username2', type=str)
#parser.add_argument('email', type=str)

class UsersListAPI(Resource):
              
    def get(self):
        users = User.query.all()
        return { 'users': marshal(users, user_fields) }


class UserAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        #self.reqparse.add_argument('email', type = str, location = 'json')
        self.reqparse.add_argument('username', type = str)
        self.reqparse.add_argument('email', type = str)
        self.reqparse.add_argument('type', type = str)
        print "1"
        super(UserAPI, self).__init__()
        
    def get_user(self, id):  
        user = User.query.get(id)
        if user is None:
            abort(404)
        else:
            return user      
        
    def get(self, id):
        user = self.get_user(id)
        return { 'user': marshal(user, user_fields) }

    def put(self, id):
        user = self.get_user(id)
        args = self.reqparse.parse_args()
        user.username = args['username']
        user.email = args['email']
        user.type = args['type']
        db.session.commit()
        return { 'user': marshal(user, user_fields) }

    def delete(self, id):
        user = self.get_user(id)
        db.session.delete(user)
        db.session.commit()
        mes = "User with id %d was deleted" % id
        return { 'mes': mes }
    
class PostAPI(Resource):
    @marshal_with(post_fields)            
    def get(self, id):
        post = Post.query.get(id);
        title = post.title
        username = post.users.username
        post.username = username
        post.test = "123"
        return  post, 201 
