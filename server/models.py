from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

convention = {
  "ix": "ix_%(column_0_label)s",
  "uq": "uq_%(table_name)s_%(column_0_name)s",
  "ck": "ck_%(table_name)s_%(constraint_name)s",
  "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
  "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)

class Author(db.Model, SerializerMixin):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    birth_year = db.Column(db.Integer)

    posts = db.relationship('Post', back_populates='author')
    

    serialize_rules = ('-posts.author',)

    def __repr__(self):
        return f"Author('{self.name}', '{self.email}', {self.birth_year})"


class Post(db.Model, SerializerMixin):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))

    author = db.relationship('Author', back_populates='posts')
    comments = db.relationship('Comment', back_populates='post')

    serialize_rules = ('-author.posts', '-comments.post',)

    def __repr__(self):
        return f"Post('{self.title}', '{self.content}')"


class Comment(db.Model, SerializerMixin):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))

    post = db.relationship('Post', back_populates='comments')
    

    serialize_rules = ('-post.comments',)

    def __repr__(self):
        return f"Comment('{self.content}')"