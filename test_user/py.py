import os
import unittest


from main import app, db
from main.models import User, Post, Category, Tags

class TestUser(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/flask2'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        #pass

    def test_posts_by_user(self):
        u = User(username = 'john', password = "123", email = 'john@example.com', type=0)
        db.session.add(u)
        db.session.commit()
        categ = Category("sports")
        db.session.add(categ)
        db.session.commit()
        list_categ=[]
        list_categ.append(categ)
        tag = Tags("sports",1)
        list_tag=[]
        db.session.add(tag)
        db.session.commit()
        list_tag.append(tag)
        post = Post("title", "excerpt", "description", "image", u.id, list_categ, list_tag)
        db.session.add(post)
        db.session.commit()
        list_posts = u.posts_by_user()
        expected =1
        assert expected == len(list_posts.all())
        
    def test_follow_user(self):
        u = User(username = 'john2', password = "123", email = 'john2@example.com', type=0)
        u1 = User(username = 'john3', password = "123", email = 'john3@example.com', type=0)
        db.session.add(u)
        db.session.add(u1)
        db.session.commit()
        user = u.follow(u1)
        if user:
            db.session.commit() 
        followers=[]
        followers.append(u1)
        assert followers == u.followed.all()  
        
    def test_unfollow_user(self):
        u = User(username = 'john2', password = "123", email = 'john2@example.com', type=0)
        u1 = User(username = 'john3', password = "123", email = 'john3@example.com', type=0)
        db.session.add(u)
        db.session.add(u1)
        db.session.commit()
        user = u.follow(u1)
        if user:
            db.session.commit() 
        user = u.unfollow(u1)
        if user:
            db.session.commit() 
        followers = []
        assert followers == u.followed.all()  
        
    def test_isfollowing(self):
        u = User(username = 'john2', password = "123", email = 'john2@example.com', type=0)
        u1 = User(username = 'john3', password = "123", email = 'john3@example.com', type=0)
        db.session.add(u)
        db.session.add(u1)
        db.session.commit()
        user = u.follow(u1)
        if user:
            db.session.commit() 
        following = u.is_following(u1)  
        assert True == following       

#if __name__ == '__main__':
#    unittest.main()