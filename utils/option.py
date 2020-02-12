from typing import Any

from sqlalchemy.orm.exc import NoResultFound

from models import db
from models.Option import Option
from utils.option_schemas.schema import SchemaMeta, OptionKey
from typeguard import check_type

class NotInSchemaError(KeyError):
    def __init__(self, k):
        super().__init__()
        self.key = k

    def __str__(self):
        if isinstance(self.key, str):
            return 'Key "' + self.key + '" is not defined in schema, maybe you forgot to set metaclass=SchemeMeta?'
        else:
            return 'Key must be a string'


class NotInitializedError(KeyError):
    def __init__(self, k):
        super().__init__()
        self.key = k

    def __str__(self):
        return 'Key "' + self.key + '" has not been initialized'


def set_option(k: OptionKey, v: Any):
    if not isinstance(k, OptionKey):
        raise TypeError('type OptionKey is expected')

    check_type('v', v, k.type)
    if k.qualified is None:
        raise NotInSchemaError(k)
    try:
        row = Option.query.filter_by(key=k.qualified).one()
        row.value = v
    except NoResultFound:
        db.session.add(Option(key=k.qualified, value=v))


def get_option(k: OptionKey) -> Any:
    if not isinstance(k, OptionKey):
        raise TypeError('type OptionKey is expected')

    if k.qualified is None:
        raise NotInSchemaError(k)
    try:
        row = Option.query.filter_by(key=k.qualified).one()
        return row.value
    except NoResultFound:
        if k.default is not None:
            return k.default
        else:
            raise NotInitializedError(k.qualified)
