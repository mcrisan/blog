from __future__ import absolute_import

from main.celery.celery import cel_app
from main.email import follower_notification
from main.models import User


@cel_app.task()
def send_email(followed_id, follower_id):
    followed= User.query.get(followed_id)
    follower = User.query.get(follower_id)
    follower_notification(followed, follower) 
    return True