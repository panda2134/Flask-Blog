from flask import abort, request
from flask.views import MethodView
from sqlalchemy.orm.exc import NoResultFound

from models.Post import Tag
from utils.api_jsonify import api_jsonify


class TagsView(MethodView):
    @staticmethod
    def get(tag: str):
        try:
            model_tag = Tag.query.filter_by(name=tag).one()
        except NoResultFound:
            abort(404)
        return api_jsonify(dict(
            (str(x.id), x.name) for x in model_tag.posts
        ))

    @staticmethod
    def search():
        if 'q' not in request.args:
            query_str = ''
        else:
            query_str = request.args['q']
        return api_jsonify({
            'tags': [x.name for x in Tag.query.filter(Tag.name.contains(query_str)).all()]
        })
