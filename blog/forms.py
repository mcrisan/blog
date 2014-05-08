from flask_wtf import Form
from flask.ext.wtf.html5 import EmailField, URLField
#from flask.ext.wtf import widgets, SelectMultipleField
from wtforms import TextField, PasswordField, TextAreaField, SelectMultipleField, widgets
from wtforms.validators import Required, url
from main.models import User, Post, Category


class LoginForm(Form):
    username = TextField('Username', validators = [Required()])
    password = PasswordField('Password', validators = [Required()])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False
        print self.username.data
        user = User.query.filter_by(username=self.username.data).first()
        if user is None:
            self.username.errors.append('Unknown username')
            return False

        if not user.password==self.password.data:
            self.password.errors.append('Invalid password')
            return False

        self.user = user
        return True
    
    
class RegisterForm(Form):
    username = TextField('Username', validators = [Required()])
    password = PasswordField('Password', validators = [Required()])
    email = EmailField('Email', validators = [Required()])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = User
    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        user1 = User.query.filter_by(username=self.username.data).first()
        #print  user    
        if user1:  
            self.username.errors.append('Username is taken')
            print "este user"
            return False
        
        user2 = User.query.filter_by(
            email=self.email.data).first()
        if user2:   
            self.email.errors.append('Email already exists')
            return False

        self.user.username = self.username.data
        self.user.password = self.password.data
        self.user.email = self.email.data
        return True    

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput() 
    
class CreatePostForm(Form):
   
    title = TextField('Title', validators = [Required()])
    excerpt = TextAreaField('Excerpt', validators = [Required()])
    description = TextAreaField('Description', validators = [Required()])
    image = URLField('Image', validators = [url()])
    tag = TextField('Tags')
    list_categ = Category.query.all()
    cat_choice = [(str(x.id), x.name) for x in list_categ]
    categories = MultiCheckboxField('Categories', choices=cat_choice)
    
    def allowed_file(self,filename):
        ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
        return '.' in filename and \
            filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
            
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.post = Post
        
    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False 
        if not self.allowed_file(self.image.data):
            self.image.errors.append('Image Type not supported') 
        return True    
  
    
class CreateCommentForm(Form):
    comment = TextAreaField('Comment', validators = [Required()])


class SearchForm(Form):
    search = TextField('search', validators = [Required()])