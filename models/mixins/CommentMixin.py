from app import db
from abc import ABC
from sqlalchemy.ext.declarative import declared_attr


class CommentMixin(ABC):
    @declared_attr
    def comments(self):
        return db.relationship('Comment', backref='page', lazy=True)
