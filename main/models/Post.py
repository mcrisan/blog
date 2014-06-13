from datetime import datetime

from main.models.AsociateTables import post_tag, post_cat
from main import db

class Post(db.Model):
    """Creates the post model
    
    Functions:
    dump_datetime -- Deserialize datetime object into string form for JSON processing.
    serialize -- Creates a dict from post object
    serialize2 -- Creates a dict from post object
    """
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    excerpt = db.Column(db.String(200))
    description = db.Column(db.Text())
    image = db.Column(db.String(100))
    created_at = db.Column(db.DateTime(), default= datetime.now())
    updated_at = db.Column(db.DateTime(), onupdate=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    categories = db.relationship('Category', secondary=post_cat,
        backref=db.backref('posts', lazy='dynamic'))
    comments = db.relationship("Comments", backref="pcomments")
    tags = db.relationship('Tags', secondary=post_tag,
        backref=db.backref('tposts', lazy='dynamic'))
    status = db.Column(db.Integer)
    
    def __init__(self, title=None, excerpt=None, description=None, 
                 image=None, user_id=None, categories=[], tags=[], status=0):
        self.title = title
        self.excerpt = excerpt
        self.description = description
        self.image = image
        self.user_id = user_id
        self.categories = categories
        self.tags = tags
        self.status = status

    def __repr__(self):
        return '%s' % self.title   
    
            
    def dump_datetime(self, value):
        """Deserialize datetime object into string form for JSON processing."""
        if value is None:
            return None
        return [value.strftime("%Y-%m-%d"), value.strftime("%H:%M:%S")]    
        
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
           'id'         : self.id,
           'title'      : self.title,
           'excerpt'    : self.excerpt,
           'description': self.description,
           'image'      : self.image,
           'created_at' : self.dump_datetime(self.created_at),
           'updated_at' : self.dump_datetime(self.updated_at)
           }  
        
    def serialize2(self):
        """Return object data in easily serializeable format"""
        return {
           'id'         : self.id,
           'title'      : self.title,
           'excerpt'    : self.excerpt,
           'description': self.description
           }       
    