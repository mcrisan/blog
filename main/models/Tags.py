from main import db
from main.models import Post

class Tags(db.Model):
    __tablename__ = 'tags'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50)) 
    count = db.Column(db.Integer) 
    
    def __init__(self, name=None, count=None):
        self.name = name 
        self.count = count   
     
    def list_of_tags(self, tags):
        tag_names = tags.split(",") 
        tag_list =[]
        for tag in tag_names:
            db_tag = Tags.query.filter_by(name=tag.lstrip()).first()    
            if db_tag:
                db_tag.count += 1
            else:
                db_tag = Tags(tag.lstrip(), 1)    
            tag_list.append(db_tag)
        return tag_list   
    
        
    def str_tags(self, tag_list):
        str_list = []
        for tag in tag_list:
            str_list.append(tag.name) 
        return ', '.join(str_list)
    
    def load_tags(self):
        query = db.session.query(Tags.name, Tags.id, db.func.count(Post.id)).join(Post.tags).group_by(Tags.id)  
        return query 