from main import db
from datetime import datetime
from main.models.Comments import Comments
from main.models.Category import Category
from main.models.Tags import Tags
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
    status = db.Column(db.Integer)
    
    def __init__(self, 
                 title=None, 
                 excerpt=None, 
                 description=None, 
                 image=None, 
                 user_id=None, 
                 categories=[], 
                 tags=[], 
                 status=0
                 ):
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
    
    @staticmethod
    def top_posts():
        return db.session.query(Post.id, Post.title, Post.image, db.func.count(Comments.post_id).label('total')) \
                         .outerjoin(Comments, ( Post.id == Comments.post_id)) \
                         .group_by(Post.id) \
                         .order_by('total DESC') \
                         .limit(3)
    
    def posts_category_status(self, cat_name, status):
        posts = Post.query.join(post_cat, Post.id==post_cat.c.post_id) \
                          .join(Category, post_cat.c.category_id == Category.id) \
                          .filter(db.and_(Category.name==cat_name, Post.status==status))
        return posts
    
    def posts_tag_status(self, tag_name, status):
        posts = Post.query.join(post_tag, Post.id==post_tag.c.post_id) \
                          .join(Tags, post_tag.c.tag_id == Tags.id) \
                          .filter(db.and_(Tags.name==tag_name, Post.status==status))
        return posts

    
    def get_comments_by_post(self):
        com = Comments.query.filter((Comments.post_id==self.id)&(Comments.parent_id==None) ) \
                            .order_by(Comments.created_at.desc()) \
                            .all()
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