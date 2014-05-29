from main.models.AsociateTables import post_cat
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
        
    def list_of_categories(self, categories):
        """Returns list of categories from a list of names
        
        Keyword arguments:
        categories -- list of category names
        """
        cat =[]
        for category in categories:
            categ = Category.query.get(category)
            cat.append(categ)
        if not categories:
            categ =  Category.query.get(3) 
            cat.append(categ)  
        return cat 
    
    @staticmethod
    def category_count():
        """Returns the number of posts for each category"""
        return db.session.query(Category.name, db.func.count(post_cat.c.category_id) \
                                .label("count")).join(post_cat, post_cat.c.category_id==Category.id) \
                                .group_by(Category.id)
