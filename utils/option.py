from sqlalchemy.orm.exc import NoResultFound

from models import db
from models.Option import Option
from typeguard import check_type

from utils.option_schemas.site import site
from utils.option_schemas.config import config

schemas = {
    **site,
    **config
}


class NotInSchemaError(KeyError):
    def __init__(self, k):
        super().__init__()
        self.key = k

    def __str__(self):
        if isinstance(self.key, str):
            return 'Key "' + self.key + '" not defined in schema'
        else:
            return 'Key must be a string'


def set_option(k, v):
    if k not in schemas:
        raise NotInSchemaError(k)
    check_type('v', v, schemas[k])
    try:
        row = Option.query.filter_by(key=k).one()
        row.value = v
    except NoResultFound:
        db.session.add(Option(key=k, value=v))


def get_option(k):
    if k not in schemas:
        raise NotInSchemaError(k)
    try:
        row = Option.query.filter_by(key=k).one()
        return row.value
    except NoResultFound:
        raise ValueError('Option "' + k + '" has not been initialized')
