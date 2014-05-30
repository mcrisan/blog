from main.models.votes import Votes

class CommentsManager():
    id =None
    
    def __init__(self, id):
        self.id = id
        
    def vote_status(self, user_id, type):
        """Returns the vote if existe and none otherwise"""
        vote = Votes.query.filter((Votes.comment_id==self.id)&(Votes.user_id==user_id)).first()
        if vote:
            if vote.type==type:
                return True
            else:
                return vote
        else:
            return None
    