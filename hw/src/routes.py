import json
from flask import Flask, request
from flasgger import Swagger
from db import db, Post, Comment

db_filename = 'posts.db'
app = Flask(__name__)

# Configuration of SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % db_filename
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SWAGGER'] = {
   "title": "Cornell AppDev - CS1998: Reddit-like Website API",
   "version": "0.0.1",
   "description": "This is the API for Cornell AppDev Fall 2018" +
   "Course CS1998: Intro to Backend Development. This API is for" +
   "a reddit-like forum website. Some links for this API:" +
   "[Course Github](https://github.com/appdev-courses) |" +
   "[Course Website](https://github.com/appdev-courses) |" +
   "[Course Piazza](https://piazza.com/class/jmb59vq5rqv2c5)"
}

# Initiation of db
db.init_app(app)
with app.app_context():
    db.create_all()

swagger = Swagger(app)

PORT = 8000

#### Code Begins Here #### 

@app.route('/api/posts/')
def get_posts():
    '''
    file: ./documentation/get_posts.yml
    '''

    posts = Post.query.all()
    res = {'success': True, 'data': [post.serialize() for post in posts]}
    return json.dumps(res), 200

@app.route('/api/posts/', methods = ['POST'])
def create_post():
    '''
    file: ./documentation/create_post.yml
    '''
    
    request_body = json.loads(request.data)
    # Code here checks for blank body requests / @beforerequests checks for None body requests
    if not request_body.get('text') == '' and not request_body.get('username') == '':
        post = Post(
            text = request_body.get('text'),
            username = request_body.get('username')
        )
        # Keep the two acts separate to reduce automatic commits to the server
        db.session.add(post)
        db.session.commit()
        return json.dumps({'success': True, 'data': post.serialize()}), 201
    return json.dumps({'success': False, 'error': 'invalid body format'}), 412

@app.route('/api/post/<int:post_id>/')
def get_post(post_id):
    '''
    file: ./documentation/get_post.yml
    '''

    post = Post.query.filter_by(id = post_id).first()
    if post is not None:
        return json.dumps({'success': True, 'data': post.serialize()}), 200
    return json.dumps({'success': False, 'error': 'Post not found!'}), 404

@app.route('/api/post/<int:post_id>/', methods = ['POST'])
def update_post(post_id):
    '''
    file: ./documentation/edit_post.yml
    '''

    post = Post.query.filter_by(id = post_id).first()
    if post is not None:
        request_body = json.loads(request.data)
        if not request_body.get('text') == '' and not request_body.get('username') == '':
            post.text = request_body.get('text', post.text)
            post.username = request_body.get('username', post.username)
            db.session.commit()
        return json.dumps({'success': True, 'data': post.serialize()}), 200
    return json.dumps({'success': False, 'error': 'Post not found!'}), 404

@app.route('/api/post/<int:post_id>/', methods = ['DELETE'])
def delete_post(post_id):
    '''
    file: ./documentation/delete_post.yml
    '''

    post = Post.query.filter_by(id = post_id).first()
    if post is not None:
        db.session.delete(post)
        db.session.commit()
        return json.dumps({'success': True, 'data': post.serialize()}), 200
    return json.dumps({'success': False, 'error': 'Post not found!'}), 404

@app.route('/api/post/<int:post_id>/comments/')
def get_comments(post_id):
    '''
    file: ./documentation/get_comments.yml
    '''

    post = Post.query.filter_by(id = post_id).first()
    if post is not None:
        comments = [comment.serialize() for comment in post.comments]
        if len(comments) != 0:
            return json.dumps({'success': True, 'data': comments}), 200
        return json.dumps({'success': True, 'data': 'There are no comments for this post.'}), 200
    return json.dumps({'success': False, 'error': 'Post not found!'}), 404

@app.route('/api/post/<int:post_id>/comment/', methods = ['POST'])
def create_comment(post_id):
    '''
    file: ./documentation/create_comment.yml
    '''

    post = Post.query.filter_by(id = post_id).first()
    if post is not None:
        request_body = json.loads(request.data)
        # Code here checks for blank body requests / @beforerequests checks for None body requests
        if not request_body.get('text') == '' and not request_body.get('username') == '':
            comment = Comment(
                text = request_body.get('text'),
                username = request_body.get('username'),
                post_id = post_id
            )
            post.comments.append(comment)
            db.session.add(comment)
            db.session.commit()
            return json.dumps({'success': True, 'data': comment.serialize()}), 201
        return json.dumps({'success': False, 'error': 'invalid body format'}), 412
    return json.dumps({'success': False, 'error': 'Post not found!'}), 404

@app.route('/api/post/<int:post_id>/vote/', methods = ['POST'])
def vote_on_post(post_id):
    '''
    file: ./documentation/vote_on_post.yml
    '''

    post = Post.query.filter_by(id = post_id).first()
    if post is not None:
        request_body = json.loads(request.data)
        # Code here checks for blank body requests / @beforerequests checks for None body requests
        if not request_body.get('vote') is None:
            # Add 1 if true / Minus 1 if false
            post.score += request_body.get('vote') * 2 - 1
            db.session.commit()
            return json.dumps({'success': True, 'data': post.serialize()}), 200
        # Magic Number 1 -> default value when body is null
        post.score += 1
        db.session.commit()
        return json.dumps({'success': True, 'data': post.serialize()}), 200
    return json.dumps({'success': False, 'error': 'Post not found!'}), 404

@app.route('/api/comment/<int:comment_id>/vote/', methods = ['POST'])
def vote_on_comment(comment_id):
    '''
    file: ./documentation/vote_on_comment.yml
    '''

    comment = Comment.query.filter_by(id = comment_id).first()
    if comment is not None:
        request_body = json.loads(request.data)
        # Code here checks for blank body requests / @beforerequests checks for None body requests
        if not request_body.get('vote') is None:
            # Add 1 if true / Minus 1 if false
            comment.score += request_body.get('vote') * 2 - 1
            db.session.commit()
            return json.dumps({'success': True, 'data': comment.serialize()}), 200
        # Magic Number 1 -> default value when body is null
        post.score += 1
        db.session.commit()
        return json.dumps({'success': True, 'data': comment.serialize()}), 200
    return json.dumps({'success': False, 'error': 'Post not found!'}), 404
# Code that checks for post requests that submit a None body

@app.before_request
def before_request():
    if request.method == 'POST':
        if request.data is None:
            return json.dumps({'success': False, 'error': 'invalid body format'}), 412


if __name__ == "__main__":
    app.run(debug=True,port=PORT)
