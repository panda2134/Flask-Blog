from typing import List
from collections import namedtuple
from .schema import get_schema

FriendLink = namedtuple('FriendLink', ['name', 'link'])
raw_schema = {
    'title': str,
    'author': str,
    'contact': dict,
    'description': str,
    'friends': List[FriendLink]
}

site = get_schema('site', raw_schema)
