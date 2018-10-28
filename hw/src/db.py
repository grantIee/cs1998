from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key = True)
    score = db.Column(db.Integer, default = 0)
    text = db.Column(db.String, nullable = False)
    username = db.Column(db.String, nullable= False)
    comments = db.relationship('Comment', cascade = 'delete')

def __init__(self, **kwags):
    self.text = kwags.get('text', '')
    self.username = kwags.get('username', '')

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
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable = False)

    def __init__(self, **kwags):
        self.text = kwags.get('text', '')
        self.username = kwags.get('username', '')
        self.task_id = kwags.get('task_id')

    def serialize(self):
        return {
            'id': self.id,
            'score': self.score,
            'text': self.text,
            'username': self.username
        }
