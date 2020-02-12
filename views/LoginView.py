from flask import request, abort
from flask.views import MethodView

from utils.auth import jwt_encode
from utils.api_jsonify import api_jsonify
from utils.option import get_option
from utils.option_schemas.config import Config

from views.CaptchaView import captcha_protected


class LoginView(MethodView):
    @staticmethod
    @captcha_protected
    def post():
        return api_jsonify({
            'token': jwt_encode(username=get_option(Config.username))
        })
