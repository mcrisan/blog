from main import db
from datetime import datetime

class Message(db.Model):
    __tablename__ = 'message'
    
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(50))
    message = db.Column(db.String(200))
    from_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    to_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    date = db.Column(db.DateTime(), default= datetime.now())

    
    def __init__(self, subject=None, message=None, from_user_id=None, to_user_id=None):
        self.subject = subject
        self.message = message
        self.from_user_id = from_user_id
        self.to_user_id = to_user_id
        self.date = datetime.now()
        
    def __repr__(self):
        return '%s' % self.subject