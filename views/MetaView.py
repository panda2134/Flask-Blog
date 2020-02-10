from typing import List
from copy import deepcopy

from flask.views import MethodView

from utils import option
from utils.option_schemas.site import FriendLink


class MetaView(MethodView):
    @staticmethod
    def get():
        pass

    @staticmethod
    def put():
        pass


class BlogMeta:
    def __init__(self, site_title_: str, author_: str, contact_: dict, friends_: List[FriendLink], description_: str):
        self.site_title = site_title_
        self.author = author_
        self.contact = contact_
        self.friends = friends_
        self.description = description_

    @staticmethod
    def from_dict(d: dict):
        friend_links = [FriendLink(name=x.name, link=x.link) for x in d['friends']]
        return BlogMeta(site_title_=d['site_title'], author_=d['author'], contact_=d['contact'],
                    friends_=friend_links, description_=d['description'])

    def to_dict(self) -> dict:
        ret = deepcopy(self.__dict__)
        print(id(ret), id(self.__dict__))
        ret['friends'] = [{'name': x.name, 'link': x.link}
                          for x in ret['friends']]
        return ret

    @staticmethod
    def read_from_options(self):
        return BlogMeta(site_title_=option.get_option('site.title'), author_=option.get_option('site.author'),
                        contact_=option.get_option('site.contact'), friends_=option.get_option('site.friends'),
                        description_=option.get_option('site.description'))

    def write_to_options(self):
        option.set_option('site.title', self.site_title)
        option.set_option('site.author', self.author)
        option.set_option('site.contact', self.contact)
        option.set_option('site.friends', self.friends)
        option.set_option('site.description', self.description)
