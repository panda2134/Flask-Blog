from datetime import datetime


def rfc3339(dt: datetime = None):
    if dt is None:
        dt = datetime.utcnow()
    return dt.isoformat() + 'Z'
