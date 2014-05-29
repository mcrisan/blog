from __future__ import absolute_import

from main.celery.celery import cel_app
from main.email import follower_notification
from main.models import User
#from main.celery import cel


@cel_app.task()
def add(x, y):
    print "calculating"
    result = x + y
    return x + y

@cel_app.task()
def send_email(followed_id, follower_id):
    print "sending"
    followed= User.query.get(followed_id)
    follower = User.query.get(follower_id)
    print (follower.username)
    follower_notification(followed, follower) 
    return True