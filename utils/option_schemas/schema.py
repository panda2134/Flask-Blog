from typeguard import check_type


class OptionKey:
    def __init__(self, type_, default_=None):
        if default_ is not None and not check_type('default_', default_, type_):
            raise TypeError(default_, type_)
        self.type = type_
        self.qualified = ''
        self.default = default_


class SchemaMeta(type):
    def __new__(mcs, name, bases, attrs):
        for k, v in attrs.items():
            if isinstance(v, OptionKey) and not attrs[k].qualified:
                attrs[k].qualified = ''.join([name.lower(), '.', k])
        return super().__new__(mcs, name, bases, attrs)
