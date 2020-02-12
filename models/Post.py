from copy import deepcopy
from datetime import datetime
from pprint import pprint

from sqlalchemy.orm.exc import NoResultFound

from models import db
from models.mixins.CommentMixin import CommentMixin
from models.mixins.TimestampMixin import TimestampMixin

from utils.rfc3339 import rfc3339

tags_assoc = db.Table('tags_assoc', db.Model.metadata,
                      db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
                      db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True)
                      )


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    posts = db.relationship('Post', back_populates='category', lazy=True)


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    posts = db.relationship('Post', secondary=tags_assoc, lazy=True, back_populates='tags')


class Post(CommentMixin, TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=False)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship(Category, back_populates='posts', lazy='subquery')
    tags = db.relationship(Tag, secondary=tags_assoc, lazy='subquery',
                           back_populates='posts')

    def comment_loc(self) -> str:
        return '/'.join(['posts', str(self.id)])

    def update_from_dict(self, modify):
        json_dict = self.to_dict()
        json_dict.update(modify)
        model_dict = Post._json_to_model_dict(json_dict)
        print(model_dict)
        self.name = model_dict['name']
        self.category = model_dict['category']
        self.tags = model_dict['tags']
        self.text = model_dict['text']
        self.updated = datetime.utcnow()

    def to_dict(self):
        return {
            'name': self.name,
            'category': self.category.name,
            'tags': [x.name for x in self.tags],
            'updated': rfc3339(self.updated),
            'text': self.text
        }

    @staticmethod
    def from_dict(d: dict):
        d = Post._json_to_model_dict(d)
        # noinspection PyArgumentList
        return Post(**d)

    @staticmethod
    def _json_to_model_dict(d: dict, auto_create=True):
        d = deepcopy(d)
        try:
            category_model = Category.query.filter_by(name=d['category']).one()
        except NoResultFound as e:
            if auto_create:
                category_model = Category(name=d['category'])
            else:
                raise e
        d['category'] = category_model

        def tag_transform(x):
            try:
                return Tag.query.filter_by(name=x).one()
            except NoResultFound:
                if auto_create:
                    return Tag(name=x)
                else:
                    raise e
        d['tags'] = [tag_transform(x) for x in d['tags']]

        return d
