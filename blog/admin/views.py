from flask.ext.admin import expose
from flask.ext.login import current_user
from flask.ext.admin.contrib.sqla import ModelView
from wtforms.fields import SelectField
from flask_security.forms import Required
from flask.ext.wtf.html5 import URLField
from flask import url_for, redirect

from main.models import Post, Tags, Category, User, Comments, Role
from main import db


   
class PostView(ModelView):       
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
            admin =Role.query.filter(Role.name=="Admin").first()
            print admin
            return current_user.has_role(admin)
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
            admin =Role.query.filter(Role.name=="Admin").first()
            print admin
            return current_user.has_role(admin)
        else:
            return False
    column_exclude_list = ['count']
    column_labels = dict(name='Tag Name')
    form_excluded_columns = ['tposts', 'count']
    form_args = dict(   
        name=dict( validators=[Required()]
        ),
                  )

    def __init__(self, session, **kwargs):
        super(TagsView, self).__init__(Tags, session, **kwargs) 
        
class CategoriesView(ModelView):
    
    def is_accessible(self):
        if current_user.is_authenticated():
            admin =Role.query.filter(Role.name=="Admin").first()
            print admin
            return current_user.has_role(admin)
        else:
            return False

    column_labels = dict(name='Category Name')
    form_excluded_columns = ['posts', ]
    form_args = dict(   
        name=dict( validators=[Required()]
        ),
                  )

    def __init__(self, session, **kwargs):
        super(CategoriesView, self).__init__(Category, session, **kwargs)  
        
class CommentsView(ModelView):
    
    def is_accessible(self):
        if current_user.is_authenticated():
            admin =Role.query.filter(Role.name=="Admin").first()
            return current_user.has_role(admin)
        else:
            return False
    column_searchable_list = ('comment', Comments.comment)
    column_labels = dict(created_at='Date', ucomments='User', pcomments='Post', children='Parent Comment')
    column_list = ('comment', 'created_at', 'likes', 'unlikes', 'ucomments', 'pcomments', 'children')
    form_excluded_columns = ['likes', 'unlikes']
    form_columns = ('comment', 'created_at', 'ucomments', 'pcomments')
    form_args = dict(   
        comment=dict( validators=[Required()]
        ),
        ucomments=dict( validators=[Required()]
        ),
        pcomments=dict( validators=[Required()]
        )
                  )
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
        