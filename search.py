from elasticsearch import Elasticsearch
from main.models import Post

es = Elasticsearch()
posts = Post.query.all()
for post in posts:
    post2 = post.serialize2()
    res = es.index(index="post", doc_type='pesan', id=post.id, body=post2)       
