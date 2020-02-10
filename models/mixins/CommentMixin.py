from sqlalchemy.ext.declarative import declared_attr

from models import db
from models.Comment import Comment


class CommentMixin:
    @declared_attr
    def comments(self):
        db.relationship(Comment, backref='page', lazy=True)