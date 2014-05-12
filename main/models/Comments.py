from main import db
from datetime import datetime
from main.models.votes import Votes

class Comments(db.Model):
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(50))  
    created_at = db.Column(db.DateTime(), default= datetime.now())  
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    parent_id = db.Column(db.Integer, db.ForeignKey('comments.id'))
    likes = db.Column(db.Integer)
    unlikes = db.Column(db.Integer)
    children = db.relationship("Comments", backref="childrenc", remote_side=[id])
    
    def __init__(self, comment, user_id, post_id, parent_id=None, likes=0, unlikes=0):
        self.comment = comment
        self.user_id = user_id
        self.post_id = post_id
        self.parent_id = parent_id
        self.likes = likes
        self.unlikes = unlikes
        
    def vote_status(self, user_id, type):
        vote = Votes.query.filter((Votes.comment_id==self.id)&(Votes.user_id==user_id)).first()
        if vote:
            if vote.type==type:
                return True
                #return "You already %s the comment" % type;
            else:
                return vote
                #vote.type = type
                #db.session.commit()
                #return "Vote modified";
        else:
            return None
            #new_vote = Votes(self.id, user_id, type)
            #db.seassion.add(new_vote)
            #db.session.commit()
            #return "New vote submitted"    