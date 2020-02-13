import string
from datetime import timedelta
from secrets import choice
from io import BytesIO
from base64 import b64encode
from functools import wraps

from jwt import InvalidTokenError
from flask import abort, request
from flask.views import MethodView
from captcha.image import ImageCaptcha

from utils import option
from utils.api_jsonify import api_jsonify
from utils.auth import jwt_encode, jwt_decode
from utils.option import get_option
from utils.option_schemas.config import Config

alphabet = list(filter(lambda x: x != 'I' and x != '1' and x != 'l'
                                 and x != '0' and x != 'O' and x != 'o',
                string.ascii_letters + string.digits))


class CaptchaView(MethodView):
    @staticmethod
    def get():
        if not option.get_option(Config.captcha):
            abort(404)
        answer = ''.join([choice(alphabet) for i in range(4)])
        captcha = ImageCaptcha().generate_image(answer)
        buf = BytesIO()
        captcha.save(buf, format='GIF')
        b64_payload = b64encode(buf.getvalue())
        payload = {
            'image': 'data:image/gif;base64,' + b64_payload.decode('ascii'),
            'answer_enc': jwt_encode(interval=timedelta(minutes=5),
                                     data={'answer': answer})
        }
        return api_jsonify(payload)

    @staticmethod
    def put():
        option.set_option(Config.captcha, request.json['enabled'])
        return api_jsonify()


def check_captcha(payload: dict) -> bool:
    if payload is None:
        return False
    try:
        jwt = jwt_decode(payload['answer_enc'])
    except InvalidTokenError:
        return False
    return jwt['data']['answer'].lower() == payload['answer'].lower()


def captcha_protected(func):
    @wraps(func)
    def wrapped_func(*args, **kwargs):
        if get_option(Config.captcha) and\
                not check_captcha(request.json.get('captcha')):
            abort(403, 'bad captcha')
        return func(*args, **kwargs)
    return wrapped_func

