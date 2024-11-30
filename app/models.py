from datetime import datetime, timezone
from hashlib import md5
from time import time
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from app import db #,login

reviews = sa.Table(
    'reviews',
    db.metadata,
    sa.Column('rating', sa.Integer, nullable=False),
    sa.Column('item_id', sa.String(36), sa.ForeignKey('item.id'))
)

class Item(db.Model):
    id = sa.Column(sa.String(36), primary_key=True)
    name = sa.Column(sa.String(64), default=None)
    description = sa.Column(sa.String(140), default=None)
    reviews = sa.Column(sa.Integer, default=0)
    photo_url = sa.Column(sa.Text(), nullable=False)

    # __table_args__ = (
    #     sa.UniqueConstraint('name', 'description', name='_name_description_uc'),
    # )

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'reviews': self.reviews,
            'photo_url': self.photo_url
        }
    
    def get_score(self):
        reviews = db.session.execute(sa.select(Rating).where(Rating.item_id == self.id)).scalars().all()
        score = 0
        for review in reviews:
            score += review.rating
        return (score/self.reviews).__round__(2) if self.reviews > 0 else 0

    def __repr__(self):
        return f'<Item {self.name}>'
    

class Rating(db.Model):
    id = sa.Column(sa.String(36), primary_key=True)
    rating = sa.Column(sa.Integer, nullable=False, default=0)
    item_id = sa.Column(sa.String(36), sa.ForeignKey('item.id'))


    def __repr__(self):
        return f'<Rating {self.id}>'
    

class User(UserMixin, db.Model):
    id = sa.Column(sa.String(36), primary_key=True)
    username = sa.Column(sa.String(64), index=True, unique=True)
    email = sa.Column(sa.String(120), index=True, unique=True)
    password_hash = sa.Column(sa.String(128))
    
    # items = so.relationship('Item', backref='author', lazy='dynamic')
    # reviews = so.relationship('Item', secondary=reviews, backref='reviewer', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def avatar(self, size: int) -> str:
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'

    def get_reset_password_token(self, expires_in: int = 600) -> str:
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        ).decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token: str) -> Optional['User']:
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
        except:
            return None
        return User.query.get(id)