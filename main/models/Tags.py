from main import db


class Tags(db.Model):
    """Creates the blog tags model
    """
    __tablename__ = 'tags' 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50)) 
    count = db.Column(db.Integer) 
    
    def __init__(self, name=None, count=None):
        self.name = name 
        self.count = count   
        
    def __repr__(self):
        return '%s' % self.name    

    
    