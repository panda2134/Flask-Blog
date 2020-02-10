from flask.views import MethodView
from flask import request, abort
from werkzeug.security import generate_password_hash

from utils import option
from models import db
from utils.option import NotInitializedError
from views.MetaView import BlogMeta


class OOBEView(MethodView):
    @staticmethod
    def get():
        try:
            option.get_option('site.title')
            abort(410)
        except NotInitializedError as e:   # database not set up properly, ok to do OOBE
            return '', 204

    @staticmethod
    def post():
        try:
            option.get_option('site.title')
            abort(410)
        except NotInitializedError as e:   # database not set up properly, ok to do OOBE
            # set up database
            from models.AboutPage import AboutPage

            # add options
            option.set_option('config.username', request.json['username'])
            option.set_option('config.passwordHash', generate_password_hash(request.json['password']))
            option.set_option('config.captcha', request.json['captcha'])

            BlogMeta.from_dict(request.json['blogMeta']).write_to_options()

            # noinspection PyArgumentList
            db.session.add(AboutPage(id=1, text=request.json['aboutPage']['text']))

            db.session.commit()


