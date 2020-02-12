import logging
from typing import List
from copy import deepcopy

from flask import request
from flask.views import MethodView

from models import db
from utils import option
from utils.api_jsonify import api_jsonify
from utils.option_schemas.site import FriendLink, Site


log = logging.getLogger('app')


class MetaView(MethodView):
    @staticmethod
    def get():
        return api_jsonify(payload=BlogMeta.load_from_options().to_dict())

    @staticmethod
    def put():
        meta_dict = BlogMeta.load_from_options().to_dict()
        meta_dict.update(request.json)
        log.debug(meta_dict)
        print(meta_dict)
        BlogMeta.from_dict(meta_dict).write_to_options()
        db.session.commit()
        return api_jsonify()


class BlogMeta:
    def __init__(self, site_title_: str, author_: str, contact_: dict, friends_: List[FriendLink], description_: str):
        self.site_title = site_title_
        self.author = author_
        self.contact = contact_
        self.friends = friends_
        self.description = description_

    @staticmethod
    def from_dict(d: dict):
        friend_links = [FriendLink(name=x['name'], link=x['link']) for x in d['friends']]
        return BlogMeta(site_title_=d['site_title'], author_=d['author'], contact_=d['contact'],
                        friends_=friend_links, description_=d['description'])

    def to_dict(self) -> dict:
        ret = deepcopy(self.__dict__)
        ret['friends'] = [{'name': x.name, 'link': x.link}
                          for x in ret['friends']]
        return ret

    @staticmethod
    def load_from_options():
        return BlogMeta(site_title_=option.get_option(Site.title), author_=option.get_option(Site.author),
                        contact_=option.get_option(Site.contact), friends_=option.get_option(Site.friends),
                        description_=option.get_option(Site.description))

    def write_to_options(self):
        option.set_option(Site.title, self.site_title)
        option.set_option(Site.author, self.author)
        option.set_option(Site.contact, self.contact)
        option.set_option(Site.friends, self.friends)
        option.set_option(Site.description, self.description)
