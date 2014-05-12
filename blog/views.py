import pprint
import json
from main import db
from blog import blog
from main.models import User, Post, Category, Comments, Tags, Votes
from flask import request, g, redirect, url_for, \
     render_template, flash, jsonify
from flask.ext.login import LoginManager, login_required, login_user, logout_user, current_user
from flask.ext.sqlalchemy import Pagination
from main import app
from blog.forms import CreatePostForm
from datetime import datetime
from elasticsearch import Elasticsearch
import re
from httplib import HTTPResponse

@blog.route('/')
@blog.route('/index', methods = ['GET', 'POST'])
@blog.route('/index/<int:page>', methods = ['GET', 'POST'])
def index(page = 1):
    posts = Post.query.order_by(Post.created_at.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False)  # @UndefinedVariable
    return render_template('index.html', posts=posts)  


@blog.route('/cat/<category>')
def posts_by_category(category):
    cat = Category.query.filter_by(name=category).first()  # @UndefinedVariable
    try:
        posts = cat.posts
    except:
        posts=""    
    return render_template('posts_categories.html', category=category, posts=posts) 


@blog.route('/tag/<tag>')
def posts_by_tag(tag):
    tags = Tags.query.filter_by(name=tag).first()  # @UndefinedVariable
    try:
        posts = tags.tposts
    except:
        posts=""    
    return render_template('post_tag.html', tag=tag, posts=posts)  


@blog.route('/user/<username>')
@blog.route('/user/<username>/<int:page>', methods = ['GET', 'POST'])
def show_user(username, page=1):
    user = User.query.filter_by(username=username).first_or_404()  # @UndefinedVariable
    #posts = user.posts_by_user().paginate(page, app.config['POSTS_PER_PAGE'], False) 
    posts = user.user_stream().paginate(page, app.config['POSTS_PER_PAGE'], False) 
    return render_template('user_details.html', user=user, posts=posts)
 
    
@blog.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = CreatePostForm()
    #flash(u'You need to login to perform the required operation') 
    if form.validate_on_submit():
        categories = form.categories.data
        tags = form.tag.data
        categ = Category()
        cat = categ.list_of_categories(categories)
        tag = Tags()
        list_tags = tag.list_of_tags(tags)
        post = Post(form.title.data, form.excerpt.data, form.description.data, form.image.data, current_user.id, cat, list_tags)
        db.session.add(post)  # @UndefinedVariable
        try:
            db.session.commit()  # @UndefinedVariable
            es = Elasticsearch()
            es.index(index="post", doc_type='pesan', id=post.id, body=post.serialize2())
            flash(u'Post was succesfully created')  
        except:
            return redirect(url_for('blog.create_post'))
        return redirect(url_for('blog.index'))       
    return render_template('create_post.html', form=form)    

    
@blog.route('/post/<id>', methods=['GET', 'POST'])
def post_details(id):
    post = Post.query.get_or_404(id)  # @UndefinedVariable
    comments =post.get_comments_by_post()
    if request.method=='POST':
        if current_user.is_authenticated():
            comment= Comments(request.form['comments'], current_user.id, post.id)
            try:
                db.session.add(comment)  # @UndefinedVariable
                db.session.commit()  # @UndefinedVariable
            except:
                return redirect(url_for('blog.post_details', id=post.id))
            return redirect(url_for('blog.post_details', id=post.id)) 
        else: 
            flash(u'You need to be logged in')              
    return render_template('post_details.html', post=post, comments=comments)
 
 
@blog.route('/create_comment', methods=['POST'])
def create_comment():
    if current_user.is_authenticated():
        id_parent = request.form['id_parent']
        id_post = request.form['id_post']
        text = request.form['text']   
        comment= Comments(text, current_user.id, id_post, id_parent)
        try:
            db.session.add(comment) 
            db.session.commit() 
        except:
            return "the operation could not be completed "            
        return render_template('comment.html', comment=comment) 
    else:
        return "-1"

@blog.route('/like_comment', methods=['GET','POST'])
def like_comment():
    if current_user.is_authenticated():
        id_comment = request.form['id_comment']
        comment = Comments.query.get(id_comment);
        vote_status = comment.vote_status(current_user.id, "like");
        print vote_status;
        if vote_status is None:
            new_vote = Votes(comment.id, current_user.id, "like")
            db.session.add(new_vote)
            db.session.commit()
            comment.likes += 1 
            db.session.commit()
            mes = "Your vote has been submitted"
        else:
            if vote_status is True:
                mes = "Your already liked the comment"
            else:
                vote_status.type = "like"
                db.session.commit()
                comment.likes += 1
                comment.unlikes -= 1
                db.session.commit() 
                mes = "Your vote has been changed"   
        return jsonify( { 'likes'        : comment.likes,
                          'unlikes'      : comment.unlikes,
                          'mes'          : mes
                         } )        
    else:
        return "-1" 
    
@blog.route('/unlike_comment', methods=['GET','POST'])
def unlike_comment():
    if current_user.is_authenticated():
        id_comment = request.form['id_comment']
        comment = Comments.query.get(id_comment);
        vote_status = comment.vote_status(current_user.id, "unlike");
        print vote_status;
        if vote_status is None:
            new_vote = Votes(comment.id, current_user.id, "unlike")
            db.session.add(new_vote)
            db.session.commit()
            comment.unlikes += 1 
            db.session.commit()
            mes = "Your vote has been submitted"
        else:
            if vote_status is True:
                mes = "Your already unliked the comment"
            else:
                vote_status.type = "unlike"
                db.session.commit()
                comment.likes -= 1
                comment.unlikes += 1
                db.session.commit()
                mes = "Your vote has been changed" 
        return jsonify( { 'likes': comment.likes,
                          'unlikes'      : comment.unlikes,
                          'mes'          : mes  
                         } )
    else:
        return "-1"     
 
@blog.route('/post/edit/<id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    post = Post.query.get_or_404(id)
    if not post.user_id == current_user.id:
        return redirect(url_for('blog.index')) 
    tag = Tags()
    categ = Category()
    tag_names = tag.str_tags(post.tags)
    categories = post.categories
    all_cat = post.check_category(categories)
    form = CreatePostForm()
    if form.validate_on_submit():
        post = Post.query.get(id)
        categories = form.categories.data
        tags = form.tag.data       
        cat = categ.list_of_categories(categories)
        list_tags = tag.list_of_tags(tags)
        post.title = form.title.data
        post.excerpt = form.excerpt.data
        post.description = form.description.data
        post.image = form.image.data
        post.categories = cat
        post.tags = list_tags
        post.updated_at = datetime.now()
        try:
            db.session.commit()
            post2 = post.serialize2()
            es = Elasticsearch()
            es.index(index="post", doc_type='pesan', id=post.id, body=post2)
            flash(u'Post was succesfully edited')  
        except:
            return redirect(url_for('blog.edit_post', id = post.id))
        return redirect(url_for('blog.post_details', id = post.id)) 
    return render_template('edit_post.html', form=form, post=post, categories=all_cat, tag_names=tag_names)    


@blog.route('/search', methods=['POST'])
def search():
    if not g.search_form.validate_on_submit():
        return redirect(url_for('blog.index'))
    return redirect(url_for('blog.search_results', query = g.search_form.search.data))


@blog.route('/search/<query>', methods=['GET', 'POST'])
def search_results(query): 
    pattern=re.compile("[^\w ']")
    new_query = pattern.sub('', query)
    es = Elasticsearch()
    res = es.search(
    index='post',
    doc_type='pesan',
    body={
      'size':10,   
      'query': {
        'query_string': {
            "fields" : ["title^5", "excerpt^2", "description"],
            "query" : "*" + new_query + "*"     
        }
      }
    })
    results=[]
    for data in res['hits']['hits']: 
        post = Post.query.get(data['_id'])
        results.append(post)    
    return render_template('post_search.html', posts=results, query = query )    

@blog.route('/autocomplete', methods=['GET', 'POST'])
def autocomplete():
    data = request.args.get('term');
    print data
    es = Elasticsearch()
    res = es.search(
    index='post',
    doc_type='pesan',
    body={
      'size':3,   
      'query': {
        'query_string': {
            "fields" : ["title^5", "excerpt^2", "description"],
            "query" : "*" + data + "*"     
        }
      }
    })
    list_title =[]
    for data in res['hits']['hits']: 
        #print data['_source']['title']
        list_title.append({
                           'title'      : data['_source']['title'],
                           'id'      : data['_source']['id']
                           } )
    print list_title    
    return jsonify( { 'posts': list_title } )    

@blog.route('/post/delete/<id>', methods=['GET', 'POST'])
@login_required
def delete_post(id):
    post = Post.query.get_or_404(id)
    if not post.user_id == current_user.id:
        return redirect(url_for('blog.index')) 
    try:
        id=post.id
        db.session.delete(post)
        db.session.commit()
        es = Elasticsearch()
        es.delete(index="post", doc_type='pesan', id=id)
        flash(u'Post was deleted')  
    except:
        return redirect(url_for('blog.post_details', id = post.id))
    return redirect(url_for('blog.index'))      
        

def render_sidebar_template():
    categories = Category.query.all()
    return render_template("sidebar.html", categories=categories)
 
