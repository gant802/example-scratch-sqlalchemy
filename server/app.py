from models import Post, Author, Comment, db
from flask import Flask, jsonify, make_response, request
from flask_migrate import Migrate
from flask_restful import Api, Resource


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

class Home(Resource):
    def get(self):
        return {"message": "Welcome to the posts API"}
    
api.add_resource(Home, '/')


#! -----------Posts routes------------------
class Posts(Resource):
    def get(self):
        posts_dict_list = [post.to_dict() for post in Post.query.all()]
        return make_response(posts_dict_list, 200)
    
    def post(self):
        data = request.get_json()
        new_post = Post(title=data['title'], content=data['content'], author_id=data['author_id'])
        db.session.add(new_post)
        db.session.commit()
        return make_response(new_post.to_dict(), 201)

api.add_resource(Posts, '/posts')

class PostsById(Resource):
    def get(self, id):
        post = Post.query.filter_by(id=id).first()
        if post:
            return make_response(post.to_dict(), 200)
        else:
            return make_response({"message": "Post not found"}, 404)

    def patch(self, id):
        data = request.get_json()
        post = Post.query.filter_by(id=id).first()
        if post:
            for attr in data:
                setattr(post, attr, data[attr])
            db.session.add(post)
            db.session.commit()
            return make_response(post.to_dict(), 200)
        else:
            return make_response({"message": "Post not found"}, 404)
        
    def delete(self, id):
        post = Post.query.filter_by(id=id).first()
        if post:
            db.session.delete(post)
            db.session.commit()
            return make_response({"message": "Post deleted"}, 200)
        else:
            return make_response({"message": "Post not found"}, 404)

api.add_resource(PostsById, '/posts/<int:id>')



#! -------------Authors routes-----------------------
class Authors(Resource):
    def get(self):
        authors_dict_list = [author.to_dict() for author in Author.query.all()]
        return make_response(authors_dict_list, 200)
    
    def post(self):
        data = request.get_json()
        new_author = Author(name=data['name'], email=data['email'], birth_year=data['birth_year'])
        db.session.add(new_author)
        db.session.commit()
        return make_response(new_author.to_dict(), 201)
    
api.add_resource(Authors, '/authors')
        
class AuthorsById(Resource):
    def get(self, id):
        author = Author.query.filter_by(id=id).first()
        if author:
            return make_response(author.to_dict(), 200)
        else:
            return make_response({"message": "Author not found"}, 404)
        
    def patch(self, id):
        data = request.get_json()
        author = Author.query.filter_by(id=id).first()
        if author:
            for attr in data:
                setattr(author, attr, data[attr])
            db.session.add(author)
            db.session.commit()
            return make_response(author.to_dict(), 200)
        else:
            return make_response({"message": "Author not found"}, 404)
        
    def delete(self, id):
        author = Author.query.filter_by(id=id).first()
        if author:
            db.session.delete(author)
            db.session.commit()
            return make_response({"message": "Author deleted"}, 200)
        else:
            return make_response({"message": "Author not found"}, 404)

api.add_resource(AuthorsById, '/authors/<int:id>')


#!---------------Comments routes------------------------
class Comments(Resource):
    def get(self):
        comments_dict_list = [comment.to_dict() for comment in Comment.query.all()]
        return make_response(comments_dict_list, 200)
    
    def post(self):
        data = request.get_json()
        new_comment = Comment(content=data['content'], author_id=data['author_id'], post_id=data['post_id'])
        db.session.add(new_comment)
        db.session.commit()
        return make_response(new_comment.to_dict(), 201)
    
api.add_resource(Comments, '/comments')

class CommentById(Resource):
    def get(self, id):
        comment = Comment.query.filter_by(id=id).first()
        if comment:
            return make_response(comment.to_dict(), 200)
        else:
            return make_response({"message": "Comment not found"}, 404)
        
    def patch(self, id):
        data = request.get_json()
        comment = Comment.query.filter_by(id=id).first()
        if comment:
            for attr in data:
                setattr(comment, attr, data[attr])
            db.session.add(comment)
            db.session.commit()
            return make_response(comment.to_dict(), 200)
        else:
            return make_response({"message": "Comment not found"}, 404)
        
    def delete(self, id):
        comment = Comment.query.filter_by(id=id).first()
        if comment:
            db.session.delete(comment)
            db.session.commit()
            return make_response({"message": "Comment deleted"}, 200)
        else:
            return make_response({"message": "Comment not found"}, 404)

api.add_resource(CommentById, '/comments/<int:id>')



if __name__ == '__main__':
    app.run(port=5555, debug=True)