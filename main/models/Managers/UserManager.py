from main.models.Post import Post
from main.models.User import User
from main import db
from main.models.AsociateTables import followers
from main.models.Comments import Comments

class UserManager(): 
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