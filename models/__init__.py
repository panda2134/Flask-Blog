from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def init_app(app):
    db.init_app(app)


def create_all():
    from models.AboutPage import AboutPage
    from models.Category import Category
    from models.Comment import Comment
    from models.Option import Option
    #from models.Tag import Tag
    from models.Post import Post

    db.create_all()
