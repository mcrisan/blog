from datetime import datetime

from main import db


class Votes(db.Model):
    """Creates the votes model"""
    __tablename__ = 'votes'   
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(), default= datetime.now())  
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    type = db.Column(db.String(50))
    
    def __init__(self, comment_id, user_id, type):
        self.comment_id = comment_id
        self.user_id = user_id
        self.type = type