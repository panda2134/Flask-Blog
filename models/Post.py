from models import db
from models.Tag import Tag
from models.TagsTable import tags_table

from models.mixins.CommentMixin import CommentMixin
from models.mixins.TimestampMixin import TimestampMixin


class Post(CommentMixin, TimestampMixin, db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=False)

    tags = db.relationship(Tag, secondary=tags_table, lazy='subquery',
                           backref=db.backref('posts', lazy=True))
