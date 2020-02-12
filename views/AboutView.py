from flask import request
from flask.views import MethodView

from utils.api_jsonify import api_jsonify
from models import db
from models.AboutPage import AboutPage


class AboutView(MethodView):
    @staticmethod
    def put():
        if 'text' in request.json:
            AboutPage.query.one().text = request.json['text']
            db.session.commit()
        return api_jsonify()

    @staticmethod
    def get():
        page: AboutPage = AboutPage.query.one()
        return api_jsonify({
            'text': page.text,
            'comment_loc': page.comment_loc()
        })
