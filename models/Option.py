from app import db


class Option(db.Model):
    key = db.Column(db.String(256), primary_key=True)
    value = db.Column(db.PickleType)
