from datetime import timedelta, timezone, datetime
from flask_sqlalchemy import SQLAlchemy
import pytz
from flask_login import UserMixin

db = SQLAlchemy()
EAT = timezone(timedelta(hours=3))

# Define the base class for all models
class Base(db.Model):
    __abstract__ = True

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.id}>'

# Define the association table for followers
followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    profile_picture = db.Column(db.String(120), default='default.jpg')
    bio = db.Column(db.Text)
    date_joined = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Africa/Nairobi')))
    posts = db.relationship('Post', backref='author', lazy='dynamic', cascade="all, delete-orphan")
    comments = db.relationship('Comment', backref='author', lazy='dynamic', cascade="all, delete-orphan")
    
    followed = db.relationship(
        'User',
        secondary=followers,
        primaryjoin=(id == followers.c.follower_id),
        secondaryjoin=(id == followers.c.followed_id),
        backref=db.backref('followers', lazy='dynamic'),
        lazy='dynamic'
    )

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            db.session.commit()

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
            db.session.commit()

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id
        ).count() > 0

class Post(Base):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(EAT))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    media_url = db.Column(db.String(120))
    likes = db.relationship('User', secondary='post_likes', backref='liked_posts')
    comments = db.relationship('Comment', backref='post', lazy='dynamic')
    post_likes = db.Table(
        'post_likes',
        db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
        db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True)
    )

class Like(Base):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False, index=True)

class Comment(Base):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

class Message(Base):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    media_url = db.Column(db.String, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    sender = db.relationship('User', foreign_keys=[sender_id], backref='sent_messages')
    recipient = db.relationship('User', foreign_keys=[recipient_id], backref='received_messages')

class Notification(Base):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(EAT))
    read = db.Column(db.Boolean, default=False)

class Follow(Base):
    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(EAT))
