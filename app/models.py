# flask shell
# u = User.query.all()
# u1, u2 = u[0], u[1]
# u1.is_following(u1)
# u1.follow(u2)
# db.session.delete()
# db.session.commit()
# db.create_all()
# db.drop_all()
import jwt

from time import time
from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
from flask_login import UserMixin
from app import db, login
from hashlib import md5
from app.search import query_index, clear_column


followers = db.Table('followers',
                     db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
                     db.Column('followed_id', db.Integer, db.ForeignKey('user.id')))


class User(UserMixin, db.Model):
    id            = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(64), index=True, unique=True)
    email         = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    posts         = db.relationship('Post', backref='author', lazy='dynamic')
    about_me      = db.Column(db.String(140))
    gender        = db.Column(db.String(10))
    last_seen     = db.Column(db.DateTime, default=datetime.utcnow)
    followed      = db.relationship('User',
                                    secondary     = followers,
                                    primaryjoin   = (followers.c.follower_id == id),
                                    secondaryjoin = (followers.c.followed_id == id),
                                    backref       = db.backref('followers', lazy='dynamic'),
                                    lazy          = 'dynamic')

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
    
    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
    
    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0
    
    def followed_posts(self):
        tracked_posts_user = Post.query.join(followers, (followers.c.followed_id  == Post.user_id)).filter(followers.c.follower_id == self.id)
        own_follow         = Post.query.filter_by(user_id=self.id)
        return tracked_posts_user.union(own_follow).order_by(Post.timestamp.desc())

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode({'reset_password': self.id, 'exp': time() + expires_in},
                          current_app.config['SECRET_KEY'], algorithm='HS256')
    
    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


class SearchableMixin:
    @classmethod
    def search(cls, expression):
        ids, ranks = query_index(cls.__searchable__, cls.__tablename__, expression)

        total = len(ids)
        if total == 0:
            return cls.query.filter_by(id=0), 0

        when = [(ids[i], i) for i in range(len(ids))]
        # return cls.query.filter(cls.id.in_(ids)).order_by(db.case(when, value=cls.id)), total
        return cls.query.filter(cls.id.in_(ids)), total
        
class Post(SearchableMixin, db.Model):
    __searchable__ = 'body'

    id        = db.Column(db.Integer, primary_key=True)
    body      = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id   = db.Column(db.Integer, db.ForeignKey('user.id'))
    language  = db.Column(db.String(5))

    def __repr__(self):
        return f'<Post {self.body}>'

@login.user_loader
def load_user(id):
    return User.query.get(int(id))