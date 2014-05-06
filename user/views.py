from user import users
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from main import db
from main.models import User
from flask.ext.login import LoginManager, login_required, login_user, logout_user, current_user
from main.email import follower_notification, email 


@users.route('/test')
@login_required
def index():
    return render_template('test.html')  


@users.route('/user/follow/<id>')
@login_required
def follow_user(id):
    follow_user= User.query.get(id)
    if follow_user == None:
        flash('User ' + follow_user.username + ' not found.')
        return redirect(url_for('blog.index'))
    if g.user == follow_user:
        flash(u"You can't follow yourself")    
        return redirect(url_for('blog.show_user', username=current_user.username))
    user = current_user.follow(follow_user)
    if user:
        db.session.commit()  
        #email()
        follower_notification(follow_user, g.user)     
        flash(u'User has been added to your followers list')
    else:
        flash(u'You already follow'+ follow_user.username)    
    return redirect(url_for('blog.show_user', username=current_user.username))


@users.route('/user/unfollow/<id>')
@login_required
def unfollow_user(id):
    unfollow_user= User.query.get(id)
    if unfollow_user == None:
        flash('User ' + unfollow_user.username + ' not found.')
        return redirect(url_for('blog.index'))
    if g.user == unfollow_user:
        flash(u"You can't unfollow yourself")    
        return redirect(url_for('blog.show_user', username=current_user.username))
    user = current_user.unfollow(unfollow_user)
    if user is None:
        flash(u'You cannot unfollow '+ unfollow_user.username)
    else:
        db.session.commit()        
        flash(u'User has been removed from your followers list')    
    return redirect(url_for('blog.show_user', username=current_user.username))
 