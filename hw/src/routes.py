from flask import Flask, request
from flasgger import Swagger
import json
import db

app = Flask(__name__)
app.config['SWAGGER'] = {
    "title": "CUAppDev - CS1998: Reddit-like Website API",
    "version": "0.0.1",
    "description": "This is the API for CUAppDev Fall 2018 Course CS1998: Intro to Backend Development. This API is for a reddit-like forum website. Some links for this API: [Course Github](https://github.com/appdev-courses) | [Course Website](https://github.com/appdev-courses) | [Course Piazza](https://piazza.com/class/jmb59vq5rqv2c5)",
}

swagger = Swagger(app)

Db = db.DB()

####Code Begins Here#### 

@app.route('/api/posts/')
def get_posts():
    '''
    file: ./documentation/get_posts.yml
    '''

    res = {'success': True, 'data': Db.get_all_posts()}
    return json.dumps(res), 200

#DONE
@app.route('/api/posts/', methods=['POST'])
def create_post():
    '''
    file: ./documentation/create_post.yml
    '''
    
    request_body = json.loads(request.data)
    #Code here checks for blank body requests / @beforerequests checks for None body requests
    if not request_body['text'] == '' and not request_body['username'] == '':
        text = request_body['text']
        username = request_body['username']
        post = {
            'id': Db.insert_post_table(text, username),
            'score': 0, 
            'text': text,
            'username': username
        }
        #INSERT CODE FOR CREATING TABLE WITH COMMENTS
        return json.dumps({'success': True, 'data': post}), 201
    return json.dumps({'success': False, 'error': 'invalid body format'}), 412

#DONE
@app.route('/api/post/<int:post_id>/')
def get_post(post_id):
    '''
    file: ./documentation/get_post.yml
    '''

    post = Db.get_post_by_id(post_id)
    if post is not None:
        return json.dumps({'success': True, 'data': post}), 200
    return json.dumps({'success': False, 'error': 'Post not found!'}), 404

#DONE
@app.route('/api/post/<int:post_id>/', methods=['POST'])
def update_post(post_id):
    '''
    file: ./documentation/edit_post.yml
    '''

    request_body = json.loads(request.data)
    text = request_body['text']
    Db.update_post_by_id(post_id, text)

    post = Db.get_post_by_id(post_id)
    if post is not None:
        return json.dumps({'success': True, 'data': post}), 200
    return json.dumps({'success': False, 'error': 'Post not found!'}), 404

#DONE
@app.route('/api/post/<int:post_id>/', methods=['DELETE'])
def delete_post(post_id):
    '''
    file: ./documentation/delete_post.yml
    '''

    post = Db.get_post_by_id(post_id)
    if post is not None:
        Db.delete_post_by_id(post_id)
        return json.dumps({'success': True, 'data': post}), 200
    return json.dumps({'success': False, 'error': 'Post not found!'}), 404

@app.route('/api/post/<int:post_id>/comments/')
def get_comments(post_id):
    '''
    file: ./documentation/get_comments.yml
    '''

    if Db.get_post_by_id(post_id) is not None:
        comments = Db.get_all_comments(post_id)
        if len(comments) != 0:
            return json.dumps({'success': True, 'data': comments}), 200
        return json.dumps({'success': True, 'data': 'There are no comments for this post.'}), 200
    return json.dumps({'success': False, 'error': 'Post not found!'}), 404

@app.route('/api/post/<int:post_id>/comment/', methods=['POST'])
def create_comment(post_id):
    '''
    file: ./documentation/create_comment.yml
    '''

    request_body = json.loads(request.data)
    #Code here checks for blank body requests / @beforerequests checks for None body requests
    if not request_body['text'] == '' and not request_body['username'] == '':
        text = request_body['text']
        username = request_body['username']
        if Db.get_post_by_id(post_id) is not None:
            comment = {
                'id': Db.insert_post_comment(text, username, post_id),
                'score': 0, 
                'text': text,
                'username': username
            }
            return json.dumps({'success': True, 'data': comment}), 201
        return json.dumps({'success': False, 'error': 'Post not found!'}), 404
    return json.dumps({'success': False, 'error': 'invalid body format'}), 412

#Code that checks for post requests that submit a None body
@app.before_request
def before_request():
    if request.method == 'POST':
        if request.data is None:
            return json.dumps({'success': False, 'error': 'invalid body format'}), 412


