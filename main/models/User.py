from datetime import datetime

from flask.ext.security import  UserMixin

from main.models.AsociateTables import followers, roles_users
from main import db


class User(db.Model, UserMixin):
    """Creates the operations a user can make
    
    Functions:
    is_active -- Returns true if the user is active
    is_anonymous -- Returns false if the user is anonymous
    is_authenticated -- Returns true if the user is loged in
    is_admin -- Returns true if the user is admin
    get_id -- Returns the id of the logged in user
    posts_by_user -- Returns a list with posts made by a user
    top_users -- Returns users with most posts
    top_comments -- Return most liked comments
    messages -- Returns messages exchange by users
    user_stream -- Returns posts from the people the user follows
    unfollow -- Unfollow a user and return the user object
    is_following --Checks if a user is following another user
    get_username_by_id -- Returns the username of the user
    """
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
    posts = db.relationship("Post", backref="users", lazy='joined')
    comments = db.relationship("Comments", backref="ucomments", lazy='joined')
    type = db.Column(db.Integer)
    followed = db.relationship('User', 
        secondary = followers, 
        primaryjoin = (followers.c.follower_id == id), 
        secondaryjoin = (followers.c.followed_id == id), 
        backref = db.backref('followers', lazy = 'dynamic'), 
        lazy = 'dynamic')
    
    def __init__(self, username=None, password=None, email=None, type=0, 
                 token=None, social=None, active=None, roles=[]):
        self.username = username
        self.password = password
        self.email = email
        self.type = type
        self.token = token
        self.social = social
        self.active = active
        self.roles = roles
        
    def __unicode__(self):
        return '%s' % self.username
    
    def is_active(self):
        """Returns true if the logged in user is active"""
        # Here you should write whatever the code is
        # that checks the database if your user is active
        return True

    def is_anonymous(self):
        """Returns false if the user is not logged in"""
        return False

    def is_authenticated(self):
        """Returns true if the user is logged in"""
        return True
    
    def is_admin(self):
        """Returns true if the logged in user is an admin"""
        if self.type == 1:
            return True
        else:
            return False
    
    def get_id(self):
        """Returns the id of the user"""
        return self.id
       
    def follow(self, user):
        """"Returns the logged in user after adding the wanted user to his followers list
        
        Keyword arguments:
        user -- the user to follow
        """
        if not self.is_following(user):
            self.followed.append(user)
            return self

    def unfollow(self, user):
        """"Returns the logged in user after removing the wanted user from his followers list
        
        Keyword arguments:
        user -- the user to remove
        """
        if self.is_following(user):
            self.followed.remove(user)
            return self

    def is_following(self, user):
        """"Returns true if the current user is following the desired user
        
        Keyword arguments:
        user -- the user to check if it is following
        """
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0
    
    def is_following_by_username(self, id):
        """"Returns true if the current user is following the desired user
        
        Keyword arguments:
        id -- the id of the user to check if it is following
        """
        return self.followed.filter(followers.c.followed_id == id).count() > 0
    
    def get_username_by_id(self, id):
        """"Returns the username of the desired user
        
        Keyword arguments:
        id -- the id of the desired user
        """
        return User.query.get(id).username