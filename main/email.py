from flask.ext.mail import Message
from main import mail
from flask import render_template
from config import ADMINS, MAIL_PASSWORD, MAIL_USERNAME, MAIL_SERVER
import smtplib
from decorators import async

@async
def send_async_email(msg):
    print "sending email 2"
    mail.send(msg)
    print "email sent"
    
def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender = sender, recipients = recipients)
    msg.body = text_body
    msg.html = html_body
    print "sending email"
    send_async_email(msg)
    #mailServer = smtplib.SMTP("smtp.gmail.com", 587, "crisan.mariusvlad@gmail.com", timeout=120)
    #mail.send(msg)
    #smtpserver = smtplib.SMTP(MAIL_SERVER, 587)
    #smtpserver.ehlo()
    #smtpserver.starttls()
    #smtpserver.ehlo
    #smtpserver.login(MAIL_USERNAME, MAIL_PASSWORD)
    #smtpserver.send(msg) 
    

def follower_notification(followed, follower):
    send_email("[microblog] %s is now following you!" % follower.username,
        ADMINS[0],
        [followed.email],
        render_template("email/follower_email.txt", 
            user = followed, follower = follower),
        render_template("email/follower_email.html", 
            user = followed, follower = follower))    
    
def email():
    message = """From: From Person <from@fromdomain.com>
    To: To Person <to@todomain.com>
    MIME-Version: 1.0
    Content-type: text/html
    Subject: SMTP HTML e-mail test

    This is an e-mail message to be sent in HTML format

    <b>This is HTML message.</b>
    <h1>This is headline.</h1>
    """

    try:
        smtpserver = smtplib.SMTP(MAIL_SERVER,587)
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.ehlo
        smtpserver.login(MAIL_USERNAME, MAIL_PASSWORD)
        smtpserver.sendmail(ADMINS[0], "crisan_marius1990@yahoo.com", message)  
        smtpserver.send(str)       
        print "Successfully sent email"
    except:
        print "Error: unable to send email"    