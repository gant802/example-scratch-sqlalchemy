from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
import re

convention = {
  "ix": "ix_%(column_0_label)s",
  "uq": "uq_%(table_name)s_%(column_0_name)s",
  "ck": "ck_%(table_name)s_%(constraint_name)s",
  "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
  "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)


#!---------------Author Class--------------------
class Author(db.Model, SerializerMixin):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False) #! unique=True is a constraint that is added at the DATABASE LEVEL
    email = db.Column(db.String, nullable=False)
    birth_year = db.Column(db.Integer)

    posts = db.relationship('Post', back_populates='author')
    
    serialize_rules = ('-posts.author',)

    @validates('name')   #! Validates input at a PYTHON LEVEL when you create an instance
    def validate_name(self, key, value):
        if not value:
            raise ValueError('Name must not be empty')
        
        return value
    
    @validates('birth_year')
    def validate_birth_year(self, key, value):
        if value < 1900 or value > 2024 or not value:
            raise ValueError('Birth year is required and must be between 1900 and 2024')
        return value
    
    @validates('email')
    def validate_email(self, key, value):
        if not value:
            raise ValueError('Email must not be empty')
        
        # Check if the email format is valid
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, value):
            raise ValueError('Invalid email address format')
        
        # Check if the email is unique
        existing_email = Author.query.filter_by(email=value).first()
        if existing_email:
            raise ValueError('Email is already in use')
        
        return value

    def __repr__(self):
        return f"Author('{self.name}', '{self.email}', {self.birth_year})"



#!--------------------Post Class------------------------
class Post(db.Model, SerializerMixin):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))

    author = db.relationship('Author', back_populates='posts')
    comments = db.relationship('Comment', back_populates='post')

    serialize_rules = ('-author.posts', '-comments.post',)

    @validates('title')
    def validate_title(self, key, value):
        if not value or len(value) > 50:
            raise ValueError('Title must not be empty and be less than 50 characters')
        return value
    
    @validates('content')
    def validate_content(self, key, value):
        if not value or len(value) > 200:
            raise ValueError('Content must not be empty and be less than 200 characters')
        return value
    
    @validates('author_id')
    def validate_author_id(self, key, value):
        existing_author = Author.query.filter_by(id = value).first()
        if not value or not existing_author:
            raise ValueError('Author ID must not be empty and be an existing author')
        return value

    def __repr__(self):
        return f"Post('{self.title}', '{self.content}')"



#!----------------Comment Class-------------------------
class Comment(db.Model, SerializerMixin):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))

    post = db.relationship('Post', back_populates='comments')
    
    serialize_rules = ('-post.comments',)

    @validates('content')
    def validate_content(self, key, value):
        if not value or len(value) > 100:
            raise ValueError('Content must not be empty and be less than 100 characters')
        return value
    
    @validates('post_id')
    def validate_ids(self, key, value):
        if not value:
            raise ValueError('Post ID must not be empty')
        existing_post = Post.query.filter_by(id=value).first()
        if not existing_post:
            raise ValueError('Post ID must be an existing post')
        return value
    
    @validates('author_id')
    def validate_author_id(self, key, value):
        if not value:
            raise ValueError('Author ID must not be empty')
        existing_author = Author.query.filter_by(id=value).first()
        if not existing_author:
            raise ValueError('Author ID must be an existing author')
        return value

    def __repr__(self):
        return f"Comment('{self.content}')"