from copy import copy
from datetime import datetime

from flask import request, abort
from flask.views import MethodView
from sqlalchemy.orm.exc import NoResultFound

from models import db
from models.Comment import Comment
from models.Post import Post, Category, Tag
from utils.api_jsonify import api_jsonify


class PostsView(MethodView):
    @staticmethod
    def get(idx: int):
        post: Post = Post.query.filter_by(id=idx).one_or_none()
        if post is None:
            abort(404)
        return api_jsonify(post.to_dict().update({'comment_loc': post.comment_loc()}))

    @staticmethod
    def post():
        req = request.json
        new_post = None
        try:
            new_post = Post.from_dict(req)
            new_post.updated = datetime.utcnow()
        except NoResultFound as e:
            abort(400, str(e))
        db.session.add(new_post)
        db.session.commit()
        return api_jsonify({
            'id': new_post.id
        })

    @staticmethod
    def search():
        if 'q' not in request.args:
            query_str = ''
        else:
            query_str = request.args['q']
        rows = (Post.query
                .filter(Post.name.contains(query_str) | Post.text.contains(query_str))
                .order_by(Post.id.desc()).paginate().items)
        post_list = [(str(x.id), x.to_dict()) for x in rows]
        post_list.sort(key=lambda x: int(x[0]))
        post_dict = {}
        for x in post_list:
            post_dict[x[0]] = x[1]
        return api_jsonify(post_dict)

    @staticmethod
    def delete(idx: int):
        post: Post = Post.query.filter_by(id=idx).one_or_none()
        if post is None:
            abort(404)
        # also delete the related category & tags; store a copy first
        category = copy(post.category)
        tags = copy(post.tags)
        loc = post.comment_loc()
        db.session.delete(post)
        db.session.flush()
        if not category.posts:
            db.session.delete(category)
        for tag in tags:
            if not tag.posts:
                db.session.delete(tag)
        Comment.query.filter_by(loc=loc).delete()
        db.session.commit()
        return api_jsonify({'id': idx})

    @staticmethod
    def put(idx: int):
        req = request.json
        post = Post.query.filter_by(id=idx).one_or_none()
        if post is None:
            abort(404)
        post.update_from_dict(req)
        db.session.add(post)
        db.session.commit()
        return api_jsonify({'id': idx})
