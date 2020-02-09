from app import db


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(320), nullable=True)
    text = db.Column(db.Text, nullable=False)
    is_spam = db.Column(db.Boolean, default=False)