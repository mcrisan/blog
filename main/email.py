from config import ADMINS, MAIL_PASSWORD
import smtplib
      

def follower_notification(followed, follower):  
    fromaddr = ADMINS[0]  
    toaddrs  = [followed.email] 
    msg = 'User %s is now following you' % follower.username  
    server = smtplib.SMTP('smtp.gmail.com:587')  
    server.ehlo()
    server.starttls()  
    server.login(ADMINS[0], MAIL_PASSWORD)  
    server.sendmail(fromaddr, toaddrs, msg)  
    server.quit() 
