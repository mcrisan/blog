from flask_wtf import Form
from wtforms import TextField, TextAreaField
from wtforms.validators import Required
from main.models import User
from flask.ext.login import current_user

class SendMessage(Form):
    to_user = TextField('To', validators = [Required()])
    subject = TextAreaField('Subject', validators = [Required()])
    message = TextAreaField('Message', validators = [Required()])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        user = User.query.filter_by(username=self.to_user.data).first()   
        if not user:  
            self.to_user.errors.append('User was not found')
            return False
        if current_user.username == self.to_user.data:
            self.to_user.errors.append("You can't enter your username")
            return False
        return True  