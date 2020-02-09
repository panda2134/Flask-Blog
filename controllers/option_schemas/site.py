from typing import List
from collections import namedtuple
from .schema import schema_factory

FriendLink = namedtuple('FriendLink', ['name', 'link'])
raw_schema = {
    'title': str,
    'author': str,
    'contact': dict,
    'description': str,
    'friends': List[FriendLink]
}


class Site(schema_factory('site', raw_schema)):
    pass
