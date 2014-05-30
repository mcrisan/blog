from user import users
from flask import request, g, redirect, url_for, \
     render_template, flash
from main import db
from main.models import User, Message, UserManager
#from flask.ext.login import login_required, current_user
from flask.ext.security import login_required, current_user
from main.email import follower_notification 

from main.celery.tasks import send_email, add

from user.forms import SendMessage
import pprint
from datetime import datetime

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
        print current_user
        follower = User.query.get(current_user.id)
        print follower.username
        #follower_notification(follow_user, g.user)
        send_email.delay(follow_user.id, follower.id)
        #send_email.delay(follow_user, g.user)
        #result = add.delay(follow_user, 2)
        #print result.get()
        #follower_notification(follow_user, g.user)     
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

@users.route('/user/send_message' , methods=['GET','POST'])
@login_required
def send_message(conv=0):
    form = SendMessage() 
    if form.validate_on_submit():
        to_user = User.query.filter(User.username == form.to_user.data).first().id 
        subject = form.subject.data 
        message = form.message.data
        from_user =  current_user.id
        message = Message(subject=subject, message=message, from_user_id=from_user, to_user_id=to_user)
        db.session.add(message)
        db.session.commit()
        flash(u'Message has been sent')
        return redirect(url_for('users.view_conversation', from_user=from_user, to_user=to_user))
    return render_template('user/send_message.html', form=form)

@users.route('/user/conversation' , methods=['POST'])
@login_required
def send_conv_response(conv=0):
    print datetime.now();
    if request.method=='POST':
        print request.form['to_user']
        to_user = User.query.filter(User.username == request.form['to_user']).first().id 
        subject = request.form['subject'] 
        message = request.form['message']
        from_user =  current_user.id
        message = Message(subject=subject, message=message, from_user_id=from_user, to_user_id=to_user)
        db.session.add(message)
        db.session.commit()
        flash(u'Message has been sent')
        return redirect(url_for('users.view_conversation', from_user=from_user, to_user=to_user))
    return redirect(url_for('users.view_conversation', from_user=from_user, to_user=to_user))        


@users.route('/user/view_messages', methods = ['GET', 'POST'])
@users.route('/user/view_messages/<int:page>', methods = ['GET', 'POST'])
@login_required
def view_messages(page = 1):
    user_m = UserManager(current_user.id)
    messages = user_m.messages().all()#.paginate(page, app.config['POSTS_PER_PAGE'], False)
    #return "111"
    return render_template('user/view_messages.html', messages=messages)

@users.route('/user/conversation/<int:from_user>/<int:to_user>', methods = ['GET', 'POST'])
@login_required
def view_conversation(from_user, to_user):
    if current_user.id == from_user:
        username = User.query.get(to_user).username
    else:
        username = User.query.get(from_user).username    
    messages = Message.query.filter(
                                    db.or_(
                                           db.and_(Message.from_user_id==from_user, Message.to_user_id==to_user), 
                                           db.and_(Message.from_user_id==to_user, Message.to_user_id==from_user))) \
                      .order_by(Message.date.desc()).all()
    #return "111"
    return render_template('user/conversation.html', messages=messages, username=username)
 
@users.route('/user/test/<id>')
@login_required
def test_user(id):
    user= User.query.get(id)
    data = user.user_stream2().all()
    pprint.pprint(data)
    return "123"