from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key = True)
    score = db.Column(db.Integer, default = 0)
    text = db.Column(db.String, nullable = False)
    username = db.Column(db.String, nullable = False)
    comments = db.relationship('Comment', cascade = 'delete')

    def __init__(self, **kwargs):
        self.text = kwargs.get('text', '')
        self.username = kwargs.get('username', '')
    
    def serialize(self):
        return {
            'id': self.id,
            'score': self.score,
            'text': self.text,
            'username': self.username
        }

class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key = True)
    score = db.Column(db.Integer, default = 0)
    text = db.Column(db.String, nullable = False)
    username = db.Column(db.String, nullable= False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable = False)

    def __init__(self, **kwargs):
        self.text = kwargs.get('text', '')
        self.username = kwargs.get('username', '')
        self.task_id = kwargs.get('task_id')

    def serialize(self):
        return {
            'id': self.id,
            'score': self.score,
            'text': self.text,
            'username': self.username
        }
