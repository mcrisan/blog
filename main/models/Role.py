from flask.ext.security import  RoleMixin

from main import db

class Role(db.Model, RoleMixin):
    """Creates the role model"""
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
    
    def __repr__(self):
        return '%s' % self.name