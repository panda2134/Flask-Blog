from models import db

from models.mixins.CommentMixin import CommentMixin
from models.mixins.TimestampMixin import TimestampMixin

tags_assoc = db.Table('tags_assoc',
                      db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
                      db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True)
                      )


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    posts = db.relationship(lambda: Post, backref='category', lazy=True)


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))


class Post(CommentMixin, TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.ForeignKey('category.id'))
    text = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=False)

    tags = db.relationship(Tag, secondary=tags_assoc, lazy='subquery',
                           backref=db.backref('posts', lazy=True))
