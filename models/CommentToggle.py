from typing import Optional
from flask import abort

from models import db


class CommentToggle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    loc = db.Column(db.String(2048))
    state = db.Column(db.Boolean, default=False)


def get_state(loc: str) -> Optional[bool]:
    toggle: CommentToggle = CommentToggle.query.filter_by(loc=loc).one_or_none()
    if toggle is not None:
        return toggle.state


def set_state(loc: str, state: bool):
    toggle: CommentToggle = CommentToggle.query.filter_by(loc=loc).one_or_none()
    if toggle is None:
        toggle = CommentToggle(loc=loc)
    toggle.state = state
    db.session.add(toggle)

