from main import db


post_cat = db.Table('post_cat',
    db.Column('category_id', db.Integer, db.ForeignKey('categories.id')),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'))
)

post_tag = db.Table('post_tag',
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id')),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'))
)

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('users.id'))
)

roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))