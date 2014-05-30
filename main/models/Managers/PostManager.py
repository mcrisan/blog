from datetime import datetime

from main.models.Comments import Comments
from main.models.Post import Post
from main.models.Category import Category
from main.models.Tags import Tags
from main.models.AsociateTables import post_tag, post_cat
from main.models.User import User
from main import db, mc

class PostManager():
    
    id = None
    def __init__(self, post_id=None):
        self.id = post_id

        
    def get_categories(self):
        key= "post%dcat" % self.id
        categories = mc.get(key)
        if not categories:
            categories = db.session.query(Category).join(post_cat, Category.id==post_cat.c.category_id). \
                                              join(Post, post_cat.c.post_id == Post.id). \
                                              filter(Post.id==self.id) 
            mc.set(key, categories.all())
        return categories
    
    def get_user_post(self, user_id):
        key= "post%duser" % self.id
        user = mc.get(key)
        if not user:
            user = User.query.get(user_id) 
            mc.set(key, user)
        return user 
    
    def get_post_comments(self):
        key= "post%dcomments" % self.id
        comments = mc.get("123")
        if not comments:
            comments = Comments.query.join(Post, Post.id==Comments.post_id).filter(Post.id==self.id).all()
            mc.set(key, comments)
        return comments  
    
    def get_post_tags(self):
        key= "post%dtags" % self.id
        tags = mc.get("123")
        if not tags:
            tags = Tags.query.join(post_tag, Tags.id==post_tag.c.tag_id).join(Post, Post.id==post_tag.c.post_id).filter(Post.id==self.id).all()
            mc.set(key, tags)
        return tags 
    
    def get_post_data(self, posts, pag=True):
        post_data=[]
        if pag is True: 
            print " is true"
            posts_list = posts.items
        else:
            posts_list = posts    
        for post in posts_list:
            post_m = PostManager(post.id)
            post_det={"post" : post,
                  "user" : post_m.get_user_post(post.user_id),
                  "categories" : post_m.get_categories(),
                  "comments" : post_m.get_post_comments(),
                  "tags"     : post_m.get_post_tags()
                  }
            post_data.append(post_det)
        if pag is True:    
            data = {"post_details" : post_data,
                    "has_prev"     : posts.has_prev,
                    "has_next"     : posts.has_next,
                    "prev_num"     : posts.prev_num,
                    "next_num"     : posts.next_num
                    }
        else:
            data = {"post_details" : post_data
                }    
        return data
            
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
        """Return list of top posts baesd on the number of comments"""
        return db.session.query(Post.id, Post.title, Post.image, db.func.count(Comments.post_id).label('total')) \
                         .outerjoin(Comments, ( Post.id == Comments.post_id)) \
                         .group_by(Post.id) \
                         .order_by('total DESC') \
                         .limit(3)
    
    def posts_category_status(self, cat_name, status):
        """Returns list of posts from a certain category based on post status.
        
        Keyword arguments:
        cat_name -- the name of the category
        status -- the status of the post
        """
        posts = Post.query.join(post_cat, Post.id==post_cat.c.post_id) \
                          .join(Category, post_cat.c.category_id == Category.id) \
                          .filter(db.and_(Category.name==cat_name, Post.status==status))
        return posts
    
    def posts_tag_status(self, tag_name, status):
        """Returns list of posts from a certain tag based on post status.
        
        Keyword arguments:
        tag_name -- the name of the tag
        status -- the status of the post
        """
        posts = Post.query.join(post_tag, Post.id==post_tag.c.post_id) \
                          .join(Tags, post_tag.c.tag_id == Tags.id) \
                          .filter(db.and_(Tags.name==tag_name, Post.status==status))
        return posts

    
    def get_comments_by_post(self):
        """Returns a list of comments from a certain post"""
        com = Comments.query.filter((Comments.post_id==self.id)&(Comments.parent_id==None) ) \
                            .order_by(Comments.created_at.desc()) \
                            .all()
        return com
    
    def check_category(self, categories):
        """Returns a list which shows categories that belong to a post
        
        Keyword arguments:
        categories -- list of categories of a certain post
        """
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