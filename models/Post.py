from app import db
from models.mixins import CommentMixin, TimestampMixin
from models.TagsTable import tags as tags_table
from models.Tag import Tag


class Post(db.Model, CommentMixin, TimestampMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    text = db.Column(db.Text, nullable=False)
    tags = db.relationship(lambda: Tag, secondary=tags_table, lazy='subquery',
                           backref=db.backref('posts', lazy=True))
