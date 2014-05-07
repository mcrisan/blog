from main import db
from datetime import datetime
from main.models.Comments import Comments
from main.models.Category import Category
from main.models.AsociateTables import post_tag, post_cat

class Post(db.Model):
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
    
    def __init__(self, title, excerpt, description, image, user_id, categories, tags):
        self.title = title
        self.excerpt = excerpt
        self.description = description
        self.image = image
        self.user_id = user_id
        self.categories = categories
        self.tags = tags
        
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
           # This is an example how to deal with Many2Many relations
           #'many2many'  : self.serialize_many2many
           }  
        
    def serialize2(self):
        """Return object data in easily serializeable format"""
        return {
           'id'         : self.id,
           'title'      : self.title,
           'excerpt'    : self.excerpt,
           'description': self.description
           #'image'      : self.image,
           #'created_at' : self.dump_datetime(self.created_at),
           #'updated_at' : self.dump_datetime(self.updated_at)
           # This is an example how to deal with Many2Many relations
           #'many2many'  : self.serialize_many2many
           }       
    
    def __repr__(self):
        return '<Post %r>' % self.title
    
    def get_comments_by_post(self):
        com = Comments.query.filter((Comments.post_id==self.id)&(Comments.parent_id==None) ).order_by(Comments.created_at.desc()).all()
        return com
    
    def check_category(self, categories):
        data =[]
        all_cat = Category.query.all()
        for category in all_cat:
            ok =False
            for p_category in categories:
                if category.name == p_category.name:
                    ok =True
                    break

            if ok:
                data.append(1)
            else:
                data.append(0)
        return data     