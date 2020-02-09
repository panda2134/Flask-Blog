from .schema import schema_factory

raw_schema = {
    'username': str,
    'passwordHash': str,
    'captcha': bool
}


class Config(schema_factory('config', raw_schema)):
    pass
