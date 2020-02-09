from datetime import datetime
from app import db
from abc import ABC


class TimestampMixin(ABC):
    __abstract__ = True
    updated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())