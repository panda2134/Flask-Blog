import jwt
from jwt import InvalidTokenError
from werkzeug.exceptions import Unauthorized

from utils import option
from config import SECRET
from datetime import datetime, timedelta
from werkzeug.security import check_password_hash

from utils.option import get_option
from utils.option_schemas.config import Config


def basic_auth(username, password, required_scopes):
    if option.get_option(Config.username) != username \
            or not check_password_hash(option.get_option(Config.passwordHash), password):
        return None
    else:
        return {'sub': username}


def jwt_encode(username: str = None, interval: timedelta = timedelta(days=1), data=None):
    if data is None:
        data = {}

    now = datetime.utcnow()
    payload = {
        'iss': 'VueBlog',
        'iat': now,
        'exp': now + interval,
        'data': data
    }
    if username is not None:
        payload.update({
            'aud': username,
            'sub': username
        })
    return jwt.encode(payload, SECRET)


def jwt_decode(token, **kwargs):
    return jwt.decode(token, key=SECRET, **kwargs)


def jwt_auth(token):
    try:
        return jwt_decode(token, audience=get_option(Config.username))
    except InvalidTokenError as e:
        raise Unauthorized from e
