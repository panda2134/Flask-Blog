from sqlalchemy.exc import ProgrammingError
from flask.views import MethodView
from flask import request
from werkzeug.security import generate_password_hash

from utils import option
from utils.option_schemas.site import FriendLink
from utils.response import ok_jsonify
from views.MetaView import BlogMeta


class OOBEView(MethodView):
    @staticmethod
    def get():
        try:
            option.get_option('site.title')
            return 'gone', 410
        except ProgrammingError as e:   # database not set up properly, ok to do OOBE
            return '', 204

    @staticmethod
    def post():
        try:
            option.get_option('site.title')
            return 'gone', 410
        except ProgrammingError as e:   # database not set up properly, ok to do OOBE
            # set up database
            from models import db, create_all
            from models.AboutPage import AboutPage
            create_all()

            # add options
            option.set_option('config.username', request.json['username'])
            option.set_option('config.passwordHash', generate_password_hash(request.json['password']))
            option.set_option('config.captcha', request.json['captcha'])

            BlogMeta.from_dict(request.json['blogMeta']).write_to_options()

            db.add(AboutPage(id=1, text=request.json['aboutPage']['text']))

            db.session.commit()


