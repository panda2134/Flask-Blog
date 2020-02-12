from flask.views import MethodView
from flask import request, abort
from werkzeug.security import generate_password_hash

from utils import option
from models import db
from utils.api_jsonify import api_jsonify
from utils.option import NotInitializedError
from utils.option_schemas.site import Site
from utils.option_schemas.config import Config
from views.MetaView import BlogMeta


class OOBEView(MethodView):
    @staticmethod
    def get():
        try:
            option.get_option(Site.title)
            abort(410)
        except NotInitializedError as e:   # database not set up properly, ok to do OOBE
            return '', 204

    @staticmethod
    def post():
        try:
            option.get_option(Site.title)
            abort(410)
        except NotInitializedError as e:   # database not set up properly, ok to do OOBE
            # set up database
            from models.AboutPage import AboutPage

            # add options
            option.set_option(Config.username, request.json['username'])
            option.set_option(Config.passwordHash, generate_password_hash(request.json['password']))
            option.set_option(Config.captcha, request.json['captcha'])

            BlogMeta.from_dict(request.json['blogMeta']).write_to_options()

            # noinspection PyArgumentList
            db.session.add(AboutPage(text=request.json['aboutPage']['text']))

            db.session.commit()
            return api_jsonify(payload=None)
