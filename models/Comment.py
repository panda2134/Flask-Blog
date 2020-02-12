from models import db


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(320), nullable=True)
    text = db.Column(db.Text, nullable=False)
    is_spam = db.Column(db.Boolean, default=False)
    loc = db.Column(db.Text, nullable=False)

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'text': self.text,
            'isSpam': self.is_spam,
        }
