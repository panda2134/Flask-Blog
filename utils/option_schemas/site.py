from typing import List
from collections import namedtuple
from .schema import SchemaMeta, OptionKey

FriendLink = namedtuple('FriendLink', ['name', 'link'])


class Site(metaclass=SchemaMeta):
    title = OptionKey(str)
    author = OptionKey(str)
    contact = OptionKey(dict)
    description = OptionKey(str)
    friends = OptionKey(List[FriendLink])
