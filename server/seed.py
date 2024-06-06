from app import app
from models import Post, Author, Comment, db


if __name__ == '__main__':
        with app.app_context():
            
            Post.query.delete()
            Author.query.delete()
            Comment.query.delete()

            a1 = Author(
                  name = "Grant",
                  email = "grant@example.com",
                  birth_year = 1997
            )
            a2 = Author(
                  name = "Tim",
                  email = "tim@example.com",
                  birth_year = 1992
            )
            a3 = Author(
                  name = "Jacob",
                  email = "jacob@example.com",
                  birth_year = 1980
            )

            db.session.add_all([a1, a2, a3])
            db.session.commit()

            p1 = Post(title="Cars", content="I love cars", author_id=2)
            p2 = Post(title="Willow Trees", content="I don't like willow trees", author_id=1)
            p3 = Post(title="Penguins", content="Penguin's are cute", author_id=3)

            db.session.add_all([p1, p2, p3])
            db.session.commit()

            c1 = Comment(content="I also love cars", post_id=1, author_id=3)
            c2 = Comment(content="Why though?", post_id=2, author_id=3)
            c3 = Comment(content="I love penguins too", post_id=3, author_id=1)

            db.session.add_all([c1, c2, c3])
            db.session.commit()