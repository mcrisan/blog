from flask.ext.login import current_user
from flask.ext.admin.contrib.sqla import ModelView
from wtforms.fields import SelectField
from flask_security.forms import Required
from wtforms import PasswordField
from flask.ext.wtf.html5 import EmailField

from main.models import Post, User, Role

        
class UserView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated():
            admin =Role.query.filter(Role.name=="Admin").first()
            print admin
            return current_user.has_role(admin)
        else:
            return False
    column_choices = {
        'type': [
            (0, 'user'),
            (1, 'admin'),
        ]
    }    
    inline_models = (Post,)
    form_overrides = dict(type=SelectField, password=PasswordField, email=EmailField)
    form_args = dict(
        type=dict(coerce=int,
            choices=[(0, 'user'), (1, 'admin')]
        ),
        password=dict(label='Password', validators=[Required()]
        ),   
        username=dict(label='Username', validators=[Required()]
        ),
        email=dict(label='Email', validators=[Required()])
                  )
    column_searchable_list = ('username', User.username)
    column_list = ('username', 'email', 'social', 'roles')
    form_columns = ('username', 'password', 'email', 'posts', 'roles')
    
    form_ajax_refs = {
        'roles': {
            'fields': (Role.name,)
        }
    }
    
    
    def __init__(self, session, **kwargs):
        super(UserView, self).__init__(User, session, **kwargs)        
