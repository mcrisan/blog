from main import db
from main.models.AsociateTables import post_cat

class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
      
    def __init__(self, name=None):
        self.name = name
        
    def __repr__(self):
        return ' %s' % self.name    
        
    def list_of_categories(self, categories):
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
        return db.session.query(Category.name, db.func.count(post_cat.c.category_id) \
                                .label("count")).join(post_cat, post_cat.c.category_id==Category.id) \
                                .group_by(Category.id)
