from models import db


class CommentToggle(db.Model):
    loc = db.Column(db.Text, primary_key=True, unique=True)
    state = db.Column(db.Boolean)


def get_state(loc: str) -> bool:
    state = CommentToggle.query.filter_by(loc=loc).one_or_none()
    if state:
        return True
    else:   # state == False or state is None
        return False


def set_state(loc: str, state: bool):
    db.session.add(CommentToggle(loc=loc, state=state))
