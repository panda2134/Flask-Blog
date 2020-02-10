from models import db
from models.mixins.CommentMixin import CommentMixin


class AboutPage(CommentMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
