from main import db
from datetime import datetime
from main.models.Post import Post
from main.models.AsociateTables import followers, roles_users
from main.models.Comments import Comments
from main.models.Message import Message
from flask.ext.security import  UserMixin
import md5
from config import app_secret

class User(db.Model, UserMixin):
    __tablename__ = "users"   
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime(), default= datetime.now())
    token = db.Column(db.Text())
    oauth_token = db.Column(db.Text())
    oauth_secret = db.Column(db.Text())
    social = db.Column(db.String(50))
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    posts = db.relationship("Post", backref="users")
    comments = db.relationship("Comments", backref="ucomments")
    type = db.Column(db.Integer)
    followed = db.relationship('User', 
        secondary = followers, 
        primaryjoin = (followers.c.follower_id == id), 
        secondaryjoin = (followers.c.followed_id == id), 
        backref = db.backref('followers', lazy = 'dynamic'), 
        lazy = 'dynamic')
    
    def __init__(self, username=None, password=None, email=None, type=0, token=None, social=None, active=None, roles=[]):
        self.username = username
        self.password = password
        self.email = email
        self.type = type
        self.token = token
        self.social = social
        self.active = active
        self.roles = roles
        
#    def get_auth_token(self):       
#        salted_password = self.password + app_secret
#        return md5.new(salted_password).hexdigest()
#        #data = [str(self.id), self.password]
#        #return self.
#
    def __unicode__(self):
        return '%s' % self.username
    
    def is_active(self):
        # Here you should write whatever the code is
        # that checks the database if your user is active
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True
    
    def is_admin(self):
        if self.type == 1:
            return True
        else:
            return False
    
    def get_id(self):
        return self.id
    
    def posts_by_user(self, status):
        return Post.query.join(User, (User.id == Post.user_id)) \
                         .filter(db.and_(User.id == self.id, Post.status==status)) \
                         .order_by(Post.created_at.desc())
    
    @staticmethod
    def top_users():
        return db.session.query(User.username, User.id, db.func.count(Post.user_id).label('total')) \
                         .outerjoin(Post, ( User.id == Post.user_id)) \
                         .group_by(User.id) \
                         .order_by('total DESC').limit(5)
    
    @staticmethod
    def top_comments():
        return db.session.query(Comments.id, 
                                Comments.comment, 
                                Comments.likes, 
                                User.username.label('username'), 
                                User.id.label('user_id'), 
                                Comments.post_id 
                                ) \
                         .join(User, User.id==Comments.user_id) \
                         .order_by('likes DESC').limit(3)
    
    def messages(self):
        m_sent_max_date= db.session \
                 .query(db.func.max(Message.date).label('last_date')) \
                 .filter(Message.from_user_id == self.id) \
                 .group_by(Message.to_user_id) \
                 .subquery('t')
        m_sent = db.session \
                 .query(Message.id, 
                        Message.subject, 
                        Message.from_user_id, 
                        Message.to_user_id, 
                        User.username.label('username'), 
                        Message.date.label("date")) \
                 .join(User, User.id ==Message.to_user_id) \
                 .filter(db.and_(Message.date == m_sent_max_date.c.last_date))
        
        m_received_max_date= db.session \
                 .query(db.func.max(Message.date).label('last_date')) \
                 .filter(Message.to_user_id == self.id) \
                 .group_by(Message.from_user_id) \
                 .subquery('t') 
        m_received = db.session \
                .query(Message.id, 
                       Message.subject, 
                       Message.from_user_id, 
                       Message.to_user_id, 
                       User.username.label('username'), 
                       Message.date.label("date")) \
                .join(User, User.id ==Message.from_user_id) \
                .filter(db.and_(Message.date == m_received_max_date.c.last_date ))
        all_messages = m_sent.union(m_received).group_by('username').order_by('date DESC')
        #query = db.session.query(m_sent.c.username).filter(db.and_(
        #                                                 Message.id == m_sent.c.id
        #                                                 ))
        return all_messages
    
    def user_stream(self, status):
        return Post.query.join(followers, (followers.c.followed_id == Post.user_id)) \
                         .filter(db.and_(followers.c.follower_id == self.id, Post.status==status)) \
                         .order_by(Post.created_at.desc())
     
    def user_stream2(self):
        return db.session.query( Post.title, Comments.comment ) \
                         .join(followers, (followers.c.followed_id == Post.user_id)) \
                         .join(Comments, (Comments.post_id == Post.id)) \
                         .filter(followers.c.follower_id == self.id) \
                         .order_by(Post.created_at.desc()) 
       
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
    
    def is_following_by_username(self, id):
        return self.followed.filter(followers.c.followed_id == id).count() > 0
    
    def get_username_by_id(self, id):
        return User.query.get(id).username