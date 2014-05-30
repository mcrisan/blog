from main import db

class Category(db.Model):
    """Creates the category model
    
    Functions:
    list_of_categories -- Returns list of categories from a list of names
    category_count -- Returns the number of posts for each category
    """
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
      
    def __init__(self, name=None):
        self.name = name
        
    def __repr__(self):
        return ' %s' % self.name    
        

