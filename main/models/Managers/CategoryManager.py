from main import db

from main.models.AsociateTables import post_cat
from main.models.Category import Category
from main.models.Post import Post

class CategoryManager():
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
    
    def category_count(self):
        """Returns the number of posts for each category"""
        return db.session.query(Category.name, db.func.count(post_cat.c.category_id) \
                                .label("count")).join(post_cat, post_cat.c.category_id==Category.id) \
                                .join(Post, post_cat.c.post_id==Post.id) \
                                .filter(Post.status==1).group_by(Category.id)