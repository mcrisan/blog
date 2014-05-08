from main import db
from main.models.Post import Post
from main.models.AsociateTables import followers
from main.models.Comments import Comments


class User(db.Model):
    __tablename__ = "users"   
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)
    token = db.Column(db.Text())
    social = db.Column(db.String(50))
    posts = db.relationship("Post", backref="users")
    comments = db.relationship("Comments", backref="ucomments")
    type = db.Column(db.Integer)
    followed = db.relationship('User', 
        secondary = followers, 
        primaryjoin = (followers.c.follower_id == id), 
        secondaryjoin = (followers.c.followed_id == id), 
        backref = db.backref('followers', lazy = 'dynamic'), 
        lazy = 'dynamic')
    
    def __init__(self, username, password, email, type=0, token=None, social=None):
        self.username = username
        self.password = password
        self.email = email
        self.type = type
        self.token = token
        self.social = social
#
    def __repr__(self):
        return '<User %r>' % self.username
    
    def is_active(self):
        # Here you should write whatever the code is
        # that checks the database if your user is active
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True
    
    def get_id(self):
        return self.id
    
    def posts_by_user(self):
        return Post.query.join(User, (User.id == Post.user_id)).filter(User.id == self.id).order_by(Post.created_at.desc())
    
    def user_stream(self):
        return Post.query.join(followers, (followers.c.followed_id == Post.user_id)).filter(followers.c.follower_id == self.id).order_by(Post.created_at.desc())
     
    def user_stream2(self):
        return db.session.query( Post.title, Comments.comment ).join(followers, (followers.c.followed_id == Post.user_id)).join(Comments, (Comments.post_id == Post.id)).filter(followers.c.follower_id == self.id).order_by(Post.created_at.desc()) 
       
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            return self

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
            return self

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0