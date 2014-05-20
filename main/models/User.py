from main import db
from main.models.Post import Post
from main.models.AsociateTables import followers
from main.models.Comments import Comments
from main.models.Message import Message

class User(db.Model):
    __tablename__ = "users"   
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)
    token = db.Column(db.Text())
    oauth_token = db.Column(db.Text())
    oauth_secret = db.Column(db.Text())
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
    
    def __init__(self, username=None, password=None, email=None, type=0, token=None, social=None):
        self.username = username
        self.password = password
        self.email = email
        self.type = type
        self.token = token
        self.social = social
#
    def __repr__(self):
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
        print self.type
        if self.type == 1:
            return True
        else:
            return False
    
    def get_id(self):
        return self.id
    
    def posts_by_user(self):
        return Post.query.join(User, (User.id == Post.user_id)).filter(User.id == self.id).order_by(Post.created_at.desc())
    
    @staticmethod
    def top_users():
        return db.session.query(User.username, User.id, db.func.count(Post.user_id).label('total')).outerjoin(Post, ( User.id == Post.user_id)).group_by(User.id).order_by('total DESC').limit(5)
    
    @staticmethod
    def top_comments():
        return db.session.query(Comments.id, Comments.comment, Comments.likes, User.username.label('username'), User.id.label('user_id'), Comments.post_id ).join(User, User.id==Comments.user_id).order_by('likes DESC').limit(3)
    
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
        print all_messages.all()
        return all_messages
    
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
    
    def is_following_by_username(self, id):
        return self.followed.filter(followers.c.followed_id == id).count() > 0
    
    def get_username_by_id(self, id):
        print id
        print User.query.get(id).username
        return User.query.get(id).username