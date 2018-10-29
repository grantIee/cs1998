import unittest
import json
import requests

# NOTE: Make sure you run 'pip install requests' in your virtualenv

# URL pointing to your local dev host
LOCAL_URL = 'http://localhost:5000'
BODY = {'text': 'Hello, World!', 'username': 'Megan'}


class TestRoutes(unittest.TestCase):

    def test_get_initial_posts(self):
        res = requests.get(LOCAL_URL + '/api/posts/')
        assert res.json()['success']

    def test_create_post(self):
        res = requests.post(LOCAL_URL + '/api/posts/', data=json.dumps(BODY))
        post = res.json()['data']
        assert res.json()['success']
        assert post['text'] == 'Hello, World!'
        assert post['username'] == 'Megan'
        assert post['score'] == 0

    def test_get__post(self):
        res = requests.post(LOCAL_URL + '/api/posts/', data=json.dumps(BODY))
        post = res.json()['data']

        res = requests.get(LOCAL_URL + '/api/post/' + str(post['id']) + '/')
        assert res.json()['data'] == post

    def test_edit_post(self):
        res = requests.post(LOCAL_URL + '/api/posts/', data=json.dumps(BODY))
        post_id = res.json()['data']['id']
        res = requests.post(LOCAL_URL + '/api/post/' + str(post_id) + '/',
                            data=json.dumps({'text': 'New text'}))
        assert res.json()['success']

        res = requests.get(LOCAL_URL + '/api/post/' + str(post_id) + '/')
        assert res.json()['data']['text'] == 'New text'

    def test_delete_post(self):
        res = requests.post(LOCAL_URL + '/api/posts/', data=json.dumps(BODY))
        post_id = res.json()['data']['id']
        res = requests.delete(LOCAL_URL + '/api/post/' + str(post_id) + '/')
        assert res.json()['success']

    def test_post_comment(self):
        res = requests.post(LOCAL_URL + '/api/posts/', data=json.dumps(BODY))
        post_id = res.json()['data']['id']
        comment = {'text': 'First comment', 'username': 'Megan'}
        res = requests.post(LOCAL_URL + '/api/post/' + str(post_id) + '/comment/',
                            data=json.dumps(comment))
        assert res.json()['success']

        res = requests.get(LOCAL_URL + '/api/post/' + str(post_id) + '/comments/')
        assert res.json()['success']
        comments = res.json()['data']
        assert len(comments) == 1
        assert comments[0]['text'] == 'First comment'
        assert comments[0]['username'] == 'Megan'

    def test_get_invalid_post(self):
        res = requests.get(LOCAL_URL + '/api/post/1000/')
        assert not res.json()['success']

    def test_edit_invalid_post(self):
        res = requests.post(LOCAL_URL + '/api/post/1000/',
                            data=json.dumps({'text': 'New text'}))
        assert not res.json()['success']

    def test_delete_invalid_post(self):
        res = requests.delete(LOCAL_URL + '/api/post/1000/')
        assert not res.json()['success']

    def test_get_comments_invalid_post(self):
        res = requests.get(LOCAL_URL + '/api/post/1000/comments/')
        assert not res.json()['success']

    def test_post_invalid_comment(self):
        res = requests.post(LOCAL_URL + '/api/post/1000/comment/', data=json.dumps(BODY))
        assert not res.json()['success']

    def test_post_id_increments(self):
        res = requests.post(LOCAL_URL + '/api/posts/', data=json.dumps(BODY))
        post_id = res.json()['data']['id']

        res2 = requests.post(LOCAL_URL + '/api/posts/', data=json.dumps(BODY))
        post_id2 = res2.json()['data']['id']

        assert post_id + 1 == post_id2


if __name__ == '__main__':
    unittest.main()
