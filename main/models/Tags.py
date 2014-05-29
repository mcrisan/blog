from main import db

class Tags(db.Model):
    """Creates the blog tags model
    
    Functions:
    list_of_tags -- Returns a list of tags.
    str_tags -- Returns all tag names as a string.
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
     
    def list_of_tags(self, tags):
        """Returns a list of tags
        
        Keyword arguments:
        tags -- string containing tags splited by comma
        """
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
        """Returns a string with tags splited by comma
        
        Keyword arguments:
        tag_list -- list of tags to be transformed
        """
        str_list = []
        for tag in tag_list:
            str_list.append(tag.name) 
        return ', '.join(str_list)
    
    