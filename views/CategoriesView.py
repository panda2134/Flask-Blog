from flask import abort, request
from flask.views import MethodView
from sqlalchemy.orm.exc import NoResultFound

from models.Post import Category
from utils.api_jsonify import api_jsonify


class CategoriesView(MethodView):
    @staticmethod
    def get(category: str):
        model_category = None
        try:
            model_category = Category.query.filter_by(name=category).one()
        except NoResultFound:
            abort(404)
        return api_jsonify(dict(
            (str(x.id), x.name) for x in model_category.posts
        ))

    @staticmethod
    def search():
        if 'q' not in request.args:
            query_str = ''
        else:
            query_str = request.args['q']
        return api_jsonify({
            'categories': [x.name for x in Category.query.filter(
                Category.name.contains(query_str)
            ).all()]
        })
