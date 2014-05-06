from main import db

class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
      
    def __init__(self, name=None):
        self.name = name
        
    def list_of_categories(self, categories):
        cat =[]
        for category in categories:
            categ = Category.query.get(category)
            cat.append(categ)
        return cat    