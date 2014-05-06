from admin import admin
from main.models import User
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from main import db
from flask.ext.login import LoginManager, login_required, login_user, logout_user, current_user


@admin.route('/')
@login_required
def index():
    users = User.query.all()  # @UndefinedVariable
    return render_template('admin/index.html', users=users)

@admin.route('/posts/<id>')
@login_required
def posts_for_user(id):
    user = User.query.get(id)  # @UndefinedVariable
    if user is None:
        posts=[]
        username=""
        flash('User does not exist')
    else:    
        username = user.username
        posts = user.posts
    return render_template('admin/posts.html', posts=posts, username=username)

@admin.route('/comments/<id>')
@login_required
def pcomments_by_user(id):
    user = User.query.get(id)  # @UndefinedVariable
    if user is None:
        posts=[]
        username=""
        flash('User does not exist')
    else:    
        username = user.username
        comments = user.comments
    return render_template('admin/comments.html', comments=comments, username=username)

@admin.before_request
def restrict_access_to_admins():
    if current_user.is_authenticated():
        if current_user.type != 1:
            flash('You need to be an admin to acees the required page')
            return redirect(url_for('blog.index'))

