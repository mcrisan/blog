import json
from flask import Flask, jsonify
from service import service
from main.models import Post
from requests import put, get
import urllib2
from elasticsearch import Elasticsearch
from flask_login import current_user

@service.route('/posts', methods = ['GET'])
def get_posts():
    es = Elasticsearch()
    posts = Post.query.all()
    post_list =[]
    for post in posts:
        post2 = post.serialize2()
        post_list.append(post2)
    json = jsonify( { 'posts': post_list } )    
    return json



@service.route('/data', methods = ['GET'])
def show_posts():
    #data = get('http://localhost:5000/service/posts')
    #page = urllib2.urlopen('http://localhost:5000/service/posts')
    #page = urllib2.urlopen('http://www.python.org/')
    data = json.dumps([1, 2, 3])
    url = 'http://date.jsontest.com/'
    req = urllib2.Request(url, None, {'Content-Type': 'application/json'})
    f = urllib2.urlopen(req)
    response = f.read()
    f.close()
    #print data["posts"][0]["title"]
    decoded_data = json.loads(response)
    print decoded_data
    print response
    print decoded_data['time']
    return response
    return "123"
    #return json.dumps(data, indent=4)