from models.__init__ import db
from .mixins import CommentMixin


class AboutPage(db.Model, CommentMixin):
    text = db.Column(db.Text, nullable=False)
