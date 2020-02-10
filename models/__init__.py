from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_models(app):
    from .AboutPage import AboutPage
    from .Comment import Comment
    from .Option import Option
    from .Post import Post
    db.init_app(app)
    db.create_all()
    db.session.commit()
