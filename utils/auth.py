import jwt
from utils import option
from config import SECRET
from datetime import datetime, timedelta
from werkzeug.security import check_password_hash


def basic_auth(username, password, scope):
    if option.get_option('config.username') != username \
            or not check_password_hash(option.get_option('config.passwordHash'), password):
        return None
    else:
        return {'sub': username}


def jwt_encode(username):
    now = datetime.utcnow()
    payload = {
        'iss': 'VueBlog',
        'aud': username,
        'sub': username,
        'iat': now,
        'exp': now + timedelta(days=1)
    }
    return jwt.encode(payload, SECRET)


def jwt_decode(token):
    return jwt.decode(token, SECRET)
