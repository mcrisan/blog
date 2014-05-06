from main import db
from datetime import datetime


class Comments(db.Model):
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(50))  
    created_at = db.Column(db.DateTime(), default= datetime.now())  
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    parent_id = db.Column(db.Integer, db.ForeignKey('comments.id'))
    children = db.relationship("Comments", backref="childrenc", remote_side=[id])
    
    def __init__(self, comment, user_id, post_id, parent_id=None):
        self.comment = comment
        self.user_id = user_id
        self.post_id = post_id
        self.parent_id = parent_id