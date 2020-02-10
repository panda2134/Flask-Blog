from datetime import datetime
from models import db


class TimestampMixin:
    updated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
