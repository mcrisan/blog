
from main import mainapp, login_manager
from main import app
from models import User, Category, Tags
from blog.forms import LoginForm, RegisterForm, SearchForm
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from main import db
from flask.ext.login import LoginManager, login_required, login_user, logout_user, current_user
import pprint
import facebook
from config import app_id, app_secret


@mainapp.route('/login', methods=['GET', 'POST'])
def login():
        form = LoginForm()
        next = request.args.get('next')
        print "your next move="
        print next
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
  
        pprint.pprint(profile)   
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
    return "123 "     

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
            user = User(username, password, email, token, social)
            db.session.add(user)           
        else:
            user.token = token 
        db.session.commit()          
        login_user(user)    
        pprint.pprint(profile['username'])   
    return redirect(url_for('blog.index')) 

@mainapp.route('/register' , methods=['GET','POST'])
def register():
    form = RegisterForm()
    if request.method == 'GET':
        return render_template('register.html', form=form)
    if form.validate_on_submit():
        user = User(form.user.username, form.user.password, form.user.email)
        user.followers.append(user)
        db.session.add(user)
        try:
            db.session.commit()
        except:
            flash('User or email already exists')
            return redirect(url_for('main.register'))
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)


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

@app.context_processor
def load_tags():
    tag = Tags()
    results = tag.load_tags()
    return dict(tags= results)
    
@app.context_processor
def sidebar():
    cat = Category.query.all()
    return dict(cat= cat)    

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500