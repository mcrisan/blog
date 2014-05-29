
CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'
app_id = '793960300632535'
app_secret  = 'd3d5157044ba795094f0742af2dce8ca'
SQLALCHEMY_DATABASE_URI = 'mysql://root@localhost/flask'

# pagination
POSTS_PER_PAGE = 5

# email server
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'crisan.mariusvlad@gmail.com'
MAIL_PASSWORD = 'pass'

# administrator list
ADMINS = ['crisan.mariusvlad@gmail.com']

# twitter

consumer_key = "QnKjgwp8A05JL6ib7JGusgF8t"
consumer_secret = "ZbHkAp0DY5msfzrUqROltfFXPkULgyaAwrJr7k4KmoMOEeWA0G"
request_token_url = 'https://api.twitter.com/oauth/request_token'
access_token_url = 'https://api.twitter.com/oauth/access_token'
authenticate_url = 'https://api.twitter.com/oauth/authenticate'
callback_uri = 'http://127.0.0.1:5000/twitter_authenticated'

# redis
REDIS_HOST = "localhost"
REDIS_PASSWORD = "password"
REDIS_PORT = 6379
REDIS_DATABASE = 5

#flask security
TOKEN_AUTHENTICATION_KEY = 'auth_token'
