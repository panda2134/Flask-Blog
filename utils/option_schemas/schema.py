def get_schema(prefix, raw_schema):
    return dict([(prefix + '.' + i[0], i[1]) for i in raw_schema.items()])