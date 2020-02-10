from models.__init__ import db
from models import Post


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    posts = db.relationship(lambda: Post, backref='category', lazy=True)
