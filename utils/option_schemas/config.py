from .schema import SchemaMeta, OptionKey


class Config(metaclass=SchemaMeta):
    username = OptionKey(str)
    passwordHash = OptionKey(str)
    captcha = OptionKey(bool)
    excerptLength = OptionKey(int)
