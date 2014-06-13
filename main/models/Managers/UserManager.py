from main import db
from main.models.Post import Post
from main.models.User import User
from main.models.AsociateTables import followers
from main.models.Comments import Comments
from main.models.Message import Message

class UserManager(): 
    """Creates the operations a user can make
    
    Functions:
    posts_by_user -- Returns a list with posts made by a user
    top_users -- Returns users with most posts
    top_comments -- Return most liked comments
    messages -- Returns messages exchange by users
    user_stream -- Returns posts from the people the user follows
    """
    id=None
    
    def __init__(self, id=None):
        self.id = id
    
    def posts_by_user(self, status):
        """Returns all posts made by user, depending on the status
        
        Keyword arguments:
        status -- the status of the user
        """
        return Post.query.join(User, (User.id == Post.user_id)) \
                         .filter(db.and_(User.id == self.id, Post.status==status)) \
                         .order_by(Post.created_at.desc())
    
    def top_users(self):
        """Returns top users based on the number of posts they've made"""               
        return db.session.query(User, User.id, db.func.count(Post.user_id).label('total')) \
                         .outerjoin(Post, ( User.id == Post.user_id)) \
                         .group_by(User.id) \
                         .order_by('total DESC').limit(5)  
                         
    def user_stream(self, status):
        """Returns posts from logged in user and the people he follows"""
        return Post.query.join(followers, (followers.c.followed_id == Post.user_id)) \
                         .filter(db.and_(followers.c.follower_id == self.id, Post.status==status)) \
                         .order_by(Post.created_at.desc())
     
    def user_stream2(self):
        return db.session.query( Post.title, Comments.comment ) \
                         .join(followers, (followers.c.followed_id == Post.user_id)) \
                         .join(Comments, (Comments.post_id == Post.id)) \
                         .filter(followers.c.follower_id == self.id) \
                         .order_by(Post.created_at.desc())   
                         
    def top_comments(self):
        """Returns comments with most likes"""
        return db.session.query(Comments.id, 
                                Comments.comment, 
                                Comments.likes, 
                                User, 
                                User.id, 
                                Comments.post_id 
                                ) \
                         .join(User, User.id==Comments.user_id) \
                         .order_by('likes DESC').limit(3)
    
    def messages(self):
        """Returns messages exchanged by users"""
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
        return all_messages                        