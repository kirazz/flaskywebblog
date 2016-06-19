from flask import current_app
from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask.ext.login import UserMixin
from . import login_manager
from datetime import datetime
import bleach
from markdown import markdown

class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    username = db.Column(db.String(64),unique=True,index=True)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(64))
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    posts = db.relationship('Post',backref='author',lazy='dynamic')
    comments = db.relationship('Comment',backref='author',lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self,paswword):
        return check_password_hash(self.password_hash,paswword)

    def __repr__(self):
        return '<User %r>'% self.username

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(64),unique=True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role %r>'% self.name

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer,primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime,index=True,default=datetime.utcnow)
    body_html = db.Column(db.Text)
    author_id =db.Column(db.Integer,db.ForeignKey('users.id'))
    post_id =db.Column(db.Integer,db.ForeignKey('posts.id'))
    comments = db.relationship('Comment',backref='post',lazy='dynamic')

#markdown form server to html
    @staticmethod
    def on_change_body(target,value,oldvalue,initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p']
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value,output_format = 'html'),
            tags=allowed_tags,strip=True))
db.event.listen(Post.body,'set',Post.on_change_body)

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer,primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime,index=True,default=datetime.utcnow)
    body_html = db.Column(db.Text)
    disabled = db.Column(db.Boolean)
    author_id =db.Column(db.Integer,db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer,db.ForeignKey('posts.id'))

#markdown form server to html
    @staticmethod
    def on_change_body(target,value,oldvalue,initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'code', 'em', 'i',
                        'strong']
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value,output_format = 'html'),
            tags=allowed_tags,strip=True))
db.event.listen(Comment.body,'set',Comment.on_change_body)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))