from app import db
from models.Option import Option
from typeguard import check_type

from .option_schemas.site import Site
from .option_schemas.config import Config

schemas = {
    **Site.get_schema(),
    **Config.get_schema()
}


class NotInSchemaError(KeyError):
    def __init__(self, k):
        self.key = k

    def __str__(self):
        if isinstance(self.key, str):
            return 'Key "' + self.key + '" not defined in schema'
        else:
            return 'Key must be a string'


def set_option(k, v):
    if k not in schemas.keys():
        raise NotInSchemaError(k)
    check_type('v', v, schemas[k])
    db.add(Option(key=k, value=v))


def get_option(k):
    if k not in schemas.keys():
        raise NotInSchemaError(k)
    return Option.query.filter_by(key=k).first().value
