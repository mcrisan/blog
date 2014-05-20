from flask.ext.admin import BaseView, expose
from flask.ext.login import current_user
from flask.ext.admin.contrib.sqla import ModelView
from wtforms.fields import SelectField
from main.models import Post, Tags, Category, User, Comments
from main import db
from flask.ext.admin.contrib.sqla import filters
from blog.forms import CreatePostForm
from flask_security.forms import Required
from wtforms import PasswordField
from flask.ext.wtf.html5 import EmailField, URLField
from flask import url_for, redirect
#from main import admin

   
class PostView(ModelView):
    #form = CreatePostForm       
    list_template = 'admin/post_list.html'
    inline_models = (Comments,)
    column_sortable_list = (('title', Post.title), ('excerpt', Post.excerpt), ('description', Post.description), ('created_at', Post.created_at))
    column_searchable_list = ('title', Post.title)
    column_list = ('title', 'excerpt', 'description', 'created_at', 'users', 'categories', 'comments', 'tags', 'status')
    column_filters = ('status',
                      'title',
                      'excerpt',
                      'description')
    column_choices = {
        'status': [
            (0, 'Pending'),
            (1, 'Approved'),
            (2, 'Rejected'),
        ]
    }
    column_labels = dict(created_at='Date', )
    form_columns = ('users', 'title', 'excerpt', 'description', 'image', 'categories', 'tags', 'comments', 'status')
    form_overrides = dict(status=SelectField, image=URLField)
    form_args = dict(
        # Pass the choices to the `SelectField`
        status=dict(coerce=int,
            choices=[(0, 'Pending'), (1, 'Approved'), (1, 'Rejected')]
        ),
        users=dict(validators=[Required()]
        ),
        title=dict( validators=[Required()]
        ),   
        excerpt=dict( validators=[Required()]
        ),
        description=dict( validators=[Required()]
        ),
        image=dict( validators=[Required()]
        )
                  )
       
    form_ajax_refs = {
        'categories': {
            'fields': (Category.name, )
        },
        'tags': {
            'fields': (Tags.name,)
        },
        'users': {
            'fields': (User.username,)
        }
    }
    
    def is_accessible(self):
        if current_user.is_authenticated():
            return current_user.is_admin()
        else:
            return False
        
    @expose('/approve/<id>')
    def approve(self, id):
        post = Post.query.get(id)
        post.status=1
        db.session.commit() 
        url = url_for('.index_view')
        return redirect(url)  
    
    @expose('/reject/<id>')
    def reject(self, id):
        post = Post.query.get(id)
        post.status=2
        db.session.commit() 
        url = url_for('.index_view')
        return redirect(url)  

    def __init__(self, session, **kwargs):
        super(PostView, self).__init__(Post, session, **kwargs) 
       
        
class TagsView(ModelView):
    
    def is_accessible(self):
        if current_user.is_authenticated():
            return current_user.is_admin()
        else:
            return False
    column_exclude_list = ['count']
    column_labels = dict(name='Tag Name')
    form_excluded_columns = ['tposts', 'count']
    form_args = dict(
        # Pass the choices to the `SelectField`   
        name=dict( validators=[Required()]
        ),
                  )
    #column = ('name')

    def __init__(self, session, **kwargs):
        super(TagsView, self).__init__(Tags, session, **kwargs) 
        
class CategoriesView(ModelView):
    
    def is_accessible(self):
        if current_user.is_authenticated():
            return current_user.is_admin()
        else:
            return False

    column_labels = dict(name='Category Name')
    form_excluded_columns = ['posts', ]
    form_args = dict(
        # Pass the choices to the `SelectField`   
        name=dict( validators=[Required()]
        ),
                  )
    #column = ('name')

    def __init__(self, session, **kwargs):
        super(CategoriesView, self).__init__(Category, session, **kwargs)  
        
class CommentsView(ModelView):
    
    def is_accessible(self):
        if current_user.is_authenticated():
            return current_user.is_admin()
        else:
            return False
    column_searchable_list = ('comment', Comments.comment)
    column_labels = dict(created_at='Date', ucomments='User', pcomments='Post', children='Parent Comment')
    column_list = ('comment', 'created_at', 'likes', 'unlikes', 'ucomments', 'pcomments', 'children')
    form_excluded_columns = ['likes', 'unlikes']
    form_columns = ('comment', 'created_at', 'ucomments', 'pcomments')
    form_args = dict(
        # Pass the choices to the `SelectField`   
        comment=dict( validators=[Required()]
        ),
        ucomments=dict( validators=[Required()]
        ),
        pcomments=dict( validators=[Required()]
        )
                  )
    #column = ('name')
    form_ajax_refs = {
        'pcomments': {
            'fields': (Post.title,)
        },
        'ucomments': {
            'fields': (User.username,)
        }
    }

    def __init__(self, session, **kwargs):
        super(CommentsView, self).__init__(Comments, session, **kwargs)                    
        