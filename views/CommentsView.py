from functools import wraps

from flask import abort, request
from flask.views import MethodView
from sqlalchemy.orm.exc import NoResultFound

from models import db
from models.Comment import Comment
from models import CommentToggle
from utils.api_jsonify import api_jsonify
from views.CaptchaView import captcha_protected

VALID_URI_REGEXP = [
    'posts/[0-9]+',
    'about'
]


def validate_uri(func):
    from re import fullmatch
    @wraps(func)
    def wrapped_func(uri, *args, **kwargs):
        if not any([(fullmatch(pattern, uri) is not None) for pattern in VALID_URI_REGEXP]):
            abort(400, 'Requested location is invalid for comments')
        return func(uri, *args, **kwargs)

    return wrapped_func


class CommentsView(MethodView):
    @staticmethod
    def all_comments():
        return api_jsonify({
            'comments': {
                'list': [x.to_dict() for x in Comment.query.all().order_by(Comment.id.desc()).paginate().items]
            }
        })

    @staticmethod
    @validate_uri
    def get_comments_in_uri(uri):
        return api_jsonify({
            'comments': {
                'enabled': CommentToggle.get_state(uri),
                'list': [x.to_dict() for x in Comment.query.filter_by(loc=uri)]
            }
        })

    @staticmethod
    @validate_uri
    @captcha_protected
    def post_comment_in_uri(uri):
        new_comment = Comment(username=request.json['username'],
                              email=request.json.get('email', ''),
                              text=request.json['text'],
                              loc=uri)
        db.session.add(new_comment)
        # TODO: Akismet
        db.session.commit()
        return api_jsonify(new_comment.to_dict())

    @staticmethod
    @validate_uri
    def toggle_comments_in_uri(uri):
        CommentToggle.set_state(uri, request.json.get('enabled', False))
        db.session.commit()
        return api_jsonify()

    @staticmethod
    @validate_uri
    def get_comment_by_id(uri, comment_id):
        return api_jsonify(payload=Comment.query.filter_by(id=comment_id).first_or_404().to_dict())

    @staticmethod
    @validate_uri
    def remove_comment_by_id(uri, comment_id):
        try:
            Comment.query.filter_by(id=comment_id).all().delete()
            return api_jsonify()
        except NoResultFound:
            abort(404)
