from functools import wraps

from flask import abort, request
from flask.views import MethodView
from urllib.parse import unquote
from sqlalchemy.orm.exc import NoResultFound

from models import db
from models.Comment import Comment
from models import CommentToggle
from utils.api_jsonify import api_jsonify
from views.CaptchaView import captcha_protected

VALID_loc_REGEXP = [
    r'posts\.[0-9]+',
    r'about'
]


def validate_and_decode_loc(func):
    from re import fullmatch
    @wraps(func)
    def wrapped_func(loc, *args, **kwargs):
        unquoted = unquote(loc)
        if not any([(fullmatch(pattern, unquoted) is not None) for pattern in VALID_loc_REGEXP]):
            abort(400, 'Requested location is invalid for comments')
        return func(unquoted, *args, **kwargs)

    return wrapped_func


class CommentsView(MethodView):
    @staticmethod
    def all_comments():
        return api_jsonify({
            'comments': {
                'list': [x.to_dict() for x in Comment.query.order_by(Comment.id.desc()).paginate().items]
            }
        })

    @staticmethod
    @validate_and_decode_loc
    def get_comments_in_loc(loc):
        state = CommentToggle.get_state(loc)
        if state is None:
            abort(404)
        return api_jsonify({
            'comments': {
                'enabled': state,
                'list': [x.to_dict() for x in Comment.query.filter_by(loc=loc)]
            }
        })

    @staticmethod
    @validate_and_decode_loc
    @captcha_protected
    def post_comment_in_loc(loc):
        state = CommentToggle.get_state(loc)
        if state is None:
            abort(404)
        elif not state:
            abort(403, 'comments are disabled')
        new_comment = Comment(username=request.json['username'],
                              email=request.json.get('email', ''),
                              text=request.json['text'],
                              loc=loc)
        db.session.add(new_comment)
        # TODO: Akismet
        db.session.commit()
        return api_jsonify(new_comment.to_dict())

    @staticmethod
    @validate_and_decode_loc
    def toggle_comments_in_loc(loc):
        CommentToggle.set_state(loc, request.json.get('enabled', False))
        db.session.commit()
        return api_jsonify()

    @staticmethod
    @validate_and_decode_loc
    def get_comment_by_id(loc, comment_id):
        return api_jsonify(payload=Comment.query.filter_by(id=comment_id).first_or_404().to_dict())

    @staticmethod
    @validate_and_decode_loc
    def remove_comment_by_id(loc, comment_id):
        try:
            db.session.delete(Comment.query.filter_by(id=comment_id).one())
            db.session.commit()
            return api_jsonify()
        except NoResultFound:
            abort(404)

    @staticmethod
    @validate_and_decode_loc
    def set_spam(loc, comment_id):
        try:
            comment: Comment= Comment.query.filter_by(id=comment_id).one()
            comment.is_spam = request.json['isSpam']
            db.session.commit()
            return api_jsonify()
        except NoResultFound:
            abort(404)
