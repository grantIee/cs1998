import os
import json
import sqlite3

# From: https://goo.gl/YzypOI
def singleton(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance

class DB(object):
    """
    DB driver for the reddit-like forum app - deals with writing entities
    to the DB and reading entities from the DB
    """

    def __init__(self):
        self.conn = sqlite3.connect("./posts.db", check_same_thread=False)
        self.create_post_table()
        self.create_comment_table()


# ===================================================
# POST FUNCTIONS
# ===================================================

    def create_post_table(self):
        try:
            self.conn.execute("""
                CREATE TABLE post (
                    ID INTEGER PRIMARY KEY,
                    SCORE INTEGER DEFAULT 0,
                    TEXT TEXT NOT NULL,
                    USERNAME TEXT NOT NULL
                );
            """)
        except Exception as e:
            print(e)

    def delete_post_table(self):
        self.conn.execute('DROP TABLE IF EXISTS post;')

    def get_all_posts(self):
        cursor = self.conn.execute('SELECT * FROM post;')
        posts = []

        for row in cursor:
            posts.append({'id': row[0], 'score': row[1], 'text': row[2], 'username': row[3]})

        return posts

    def insert_post_table(self, text, username):
        cur = self.conn.cursor()
        cur.execute('INSERT INTO post (TEXT, USERNAME) VALUES (?, ?);', 
            (text, username))
        self.conn.commit()
        return cur.lastrowid

    def get_post_by_id(self, id):
        cursor = self.conn.execute('SELECT * FROM post WHERE ID == ?', (id,))

        for row in cursor:
            return {'id': row[0], 'score': row[1], 'text': row[2], 'username': row[3]}

        return None

    def update_post_by_id(self, id, text):
        self.conn.execute("""
            UPDATE post 
            SET TEXT = ?
            WHERE ID = ?;
        """, (text, id))
        self.conn.commit()

    def delete_post_by_id(self, id):
        self.conn.execute("""
            DELETE FROM post
            WHERE id = ?;        
        """, (id,))
        self.conn.commit()


# ===================================================
# COMMENT FUNCTIONS
# ===================================================

    def create_comment_table(self):
        try:
            self.conn.execute("""
                CREATE TABLE comment (
                    ID INTEGER PRIMARY KEY,
                    SCORE INTEGER DEFAULT 0,
                    TEXT TEXT NOT NULL,
                    USERNAME TEXT NOT NULL,
                    POST_ID INTEGER NOT NULL,
                    FOREIGN KEY(POST_ID) REFERENCES post(ID)
                );
            """)
        except Exception as e:
            print(e)

    def delete_comment_table(self):
        self.conn.execute('DROP TABLE IF EXISTS comment;')

    def get_all_comments(self,id):
        cursor = self.conn.execute('SELECT comment.ID, comment.SCORE, comment.TEXT, comment.USERNAME FROM comment INNER JOIN post ON comment.POST_ID = post.ID WHERE post.ID = ?;', (id,))
        comments = []

        for row in cursor:
            comments.append({'id': row[0], 'score': row[1], 'text': row[2], 'username': row[3]})

        return comments
    
    def insert_post_comment(self, text, username, id):
        cur = self.conn.cursor()
        cur.execute('INSERT INTO comment (TEXT, USERNAME, POST_ID) VALUES (?, ?, ?);', 
            (text, username, id))
        self.conn.commit()
        return cur.lastrowid
        

# Only <=1 instance of the DB driver
# exists within the app at all times
DB = singleton(DB)
