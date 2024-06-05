# This file is part of the Prodeimat project
# @Author: Ricel Quispe

# defines the SQLAlchemy database models for database
# SQLAlchemy is a popular sql toolkit and object-relational mapping (ORM) system for Python
from .database import db
from flask_login import UserMixin
from datetime import datetime

class Article(db.Model):
    __tablename__ = 'article'
    nid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    link = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(10), default='user')
    is_active = db.Column(db.Boolean, default=True) 

    def get_id(self):
        return str(self.id)
