
from main import mainapp, login_manager
from main import user_datastore, security
from main import app
from models import User, Category, Tags, Comments, Post, Role
from blog.forms import LoginForm, RegisterForm, SearchForm
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from main import db
#from flask.ext.login import LoginManager, login_required, login_user, logout_user, current_user
from flask.ext.security import login_required, login_user, logout_user, current_user
import pprint
import facebook
from config import app_id, app_secret, consumer_key, consumer_secret, request_token_url, access_token_url, authenticate_url, callback_uri
import oauth2 as oauth
import cgi
import twitter
import webbrowser
import urllib

@mainapp.route('/user_login', methods=['GET', 'POST'])
def user_login():
        form = LoginForm()
        next = request.args.get('next')
        if form.validate_on_submit():
            flash('Successfully logged in as %s' % form.user.username)
            session['user_id'] = form.user.id
            user = User.query.get(form.user.id)
            login_user(user)
            if next != "None":
                return redirect(next)
            else:
                return redirect(url_for('blog.index'))
            #return (redirect(next)  or url_for('blog.index'))
        return render_template('login.html', form=form)

@security.login_context_processor
def security_context_processor():
    form = LoginForm()
    return dict(form=form)

@mainapp.route('/ftest', methods=['GET', 'POST'])
def ftest():
    user = User.query.get(2)
    if user:
        token = user.token
        graph = facebook.GraphAPI(token)
        attachment = {"name": "Nature at it;s best",
                       "link": "newsm8.com",
                       "caption": "actor posted a new review",
                       "description": "This is a longer description of the attachment",
                       "picture": "http://www.seeanz.com/images/albino-wallaby.jpg"}
        graph.put_wall_post("Nature at it;s best", attachment)
        profile = graph.get_object("me")  
    return "123 "

@mainapp.route('/ftest2', methods=['GET', 'POST'])
def ftest2():
    user = User.query.get(2)
    if user:
        token = user.token
        graph = facebook.GraphAPI(token)
        pages = graph.get_object("me/accounts")
  
        pprint.pprint(pages["data"]) 
    return render_template('facebook_pages.html', pages=pages["data"])          

@mainapp.route('/facebook_login', methods=['GET', 'POST'])
def facebook_login():
    user = facebook.get_user_from_cookie(request.cookies, app_id, app_secret)
    if user:
        graph = facebook.GraphAPI(user["access_token"])
        profile = graph.get_object("me")
        username = profile['username']
        password = "wewesdfe"
        email = profile['email']
        token = user["access_token"]
        social = "facebook"
        
        user = User.query.filter_by(username=username).first()
        if not user:
            role = Role.query.filter(Role.name=="User").first()
            user = user_datastore.create_user(username=username, email=email, password=password, token=token, social=social)
            user_datastore.add_role_to_user(user, role)
            #user = User(username, password, email, token, social)
            #db.session.add(user)           
        else:
            user.token = token 
        db.session.commit()          
        login_user(user)       
    return redirect(url_for('blog.index')) 


@mainapp.route('/twitter_login', methods=['GET', 'POST'])
def twitter_login():
    #api = twitter.Api(consumer_key=consumer_key,
    #                  consumer_secret=consumer_secret,
    #                  access_token_key='917529883-YRxS1ByvKrMHnr9vMN7oGNTNLqo5hDeABaqg821V',
    #                  access_token_secret='j3ImOxL91rKlAi16xFjSr87YseB00MsQqzFlydp4sMZIx')
    #print api.VerifyCredentials()
    consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)
    client = oauth.Client(consumer)
    body = urllib.urlencode(dict(oauth_callback=callback_uri))   
    resp, content = client.request(request_token_url, "POST", body=body)

    if resp['status'] != '200':
        raise Exception("Invalid response from Twitter.")

    session['request_token'] = dict(cgi.parse_qsl(content))
    print "session is"
    print session['request_token']
    url = "%s?oauth_token=%s" % (authenticate_url,
        session['request_token']['oauth_token'])
    return redirect(url) 


@mainapp.route('/twitter_authenticated', methods=['GET', 'POST'])
def twitter_authenticated():
    pincode = request.args.get('oauth_verifier')
    print "12232"
    print pincode
    consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)
    token = oauth.Token(session['request_token']['oauth_token'],
                        session['request_token']['oauth_token_secret'])
    client = oauth.Client(consumer, token)

    # Step 2. Request the authorized access token from Twitter.
    body = urllib.urlencode({'oauth_callback': callback_uri, 'oauth_verifier': pincode })
    resp, content = client.request(access_token_url, "POST", body=body)
    if resp['status'] != '200':
        raise Exception("Invalid response from Twitter."+ resp['status'])

    """
    This is what you'll get back from Twitter. Note that it includes the
    user's user_id and screen_name.
    {
        'oauth_token_secret': 'IcJXPiJh8be3BjDWW50uCY31chyhsMHEhqJVsphC3M',
        'user_id': '120889797', 
        'oauth_token': '120889797-H5zNnM3qE0iFoTTpNEHIz3noL9FKzXiOxwtnyVOD',
        'screen_name': 'heyismysiteup'
    }
    """
    access_token = dict(cgi.parse_qsl(content))   
    user = User.query.filter_by(username=access_token['screen_name']).first()
    if user is None:
        role = Role.query.filter(Role.name=="User").first()
        user = user_datastore.create_user(username=access_token['screen_name'], email="email", password="234")
        user_datastore.add_role_to_user(user, role)
        #user = User(access_token['screen_name'], "234", "email", type=0)
        user.oauth_token = access_token['oauth_token']
        user.oauth_secret = access_token['oauth_token_secret']
        user.social = "twitter"
        #db.session.add(user)
        db.session.commit()
    login_user(user)
    return redirect(url_for('blog.index'))  

@mainapp.route('/register' , methods=['GET','POST'])
def register():
    form = RegisterForm()
    if request.method == 'GET':
        return render_template('register.html', form=form)
    if form.validate_on_submit():
        role = Role.query.filter(Role.name=="User").first()
        user = user_datastore.create_user(username=form.user.username, email=form.user.email, password=form.user.password)
        user_datastore.add_role_to_user(user, role)
        try:
            db.session.commit()
        except:
            flash('User or email already exists')
            return redirect(url_for('main.register'))
        return redirect(url_for('main.user_login'))
    return render_template('register.html', form=form)

@mainapp.route('/top_users' , methods=['GET','POST'])
def top_users():
    top_users = User.top_users()
    top_posts = Post.top_posts()
    top_comments = User.top_comments()
    #pprint.pprint(top_comments.all())
    Category.posts_without_cat()
    #return top_users.all()
    return render_template('top_users.html', users=top_users)

@mainapp.route("/logout")
@login_required
def logout():
    logout_user()
    session['logged_in'] = False
    return redirect(url_for('blog.index'))

@login_manager.user_loader
def load_user(userid):
    u = User.query.get(userid)
    return u #User(u.name,u.id,u.email)

@app.before_request
def before_request():
    g.user = current_user
    g.search_form = SearchForm()

@app.before_request    
def check_for_admin(*args, **kw):
    if request.path.startswith('/admin/'):
        if current_user.is_authenticated():
            if not current_user.is_admin():
                return redirect(url_for('main.login'))
        else:
            return redirect(url_for('main.login'))    

@app.context_processor
def load_sidebar():
    #tag = Tags()
    #results = tag.load_tags()
    results = Tags.query.all()
    top_users = User.top_users().all()
    top_posts = Post.top_posts().all()
    top_comments = User.top_comments().all()
    cat = Category.category_count().all()
    #posts_in_categ = 
    return dict(tags= results, users=top_users, posts2=top_posts, top_comments=top_comments, categ=cat)   

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500