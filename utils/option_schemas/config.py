from .schema import get_schema

raw_schema = {
    'username': str,
    'passwordHash': str,
    'captcha': bool
}

config = get_schema('config', raw_schema)