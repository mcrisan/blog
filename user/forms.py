from flask_wtf import Form
from flask.ext.wtf.html5 import EmailField, URLField
#from flask.ext.wtf import widgets, SelectMultipleField
from wtforms import TextField, PasswordField, TextAreaField, SelectMultipleField, widgets, HiddenField
from wtforms.validators import Required, url
from main.models import User, Post, Category
from flask.ext.login import current_user

class SendMessage(Form):
    to_user = TextField('To', validators = [Required()])
    subject = TextAreaField('Subject', validators = [Required()])
    message = TextAreaField('Message', validators = [Required()])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        #self.user = User
    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        user = User.query.filter_by(username=self.to_user.data).first()
        #print  user    
        if not user:  
            self.to_user.errors.append('User was not found')
            return False
        if current_user.username == self.to_user.data:
            self.to_user.errors.append("You can't enter your username")
            return False
        return True  