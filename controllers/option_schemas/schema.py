def schema_factory(prefix, raw_schema):
    class Schema:
        @classmethod
        def get_schema(cls):
            return dict([(prefix + '.' + i[0], i[1]) for i in raw_schema.items()])

    return Schema
