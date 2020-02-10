from controllers import Option
from flask_restful import reqparse, Resource


class OOBE(Resource):
    def get(self):
        try:
            Option.get_option('site.title')
            return 'gone', 410
        except ValueError as e:
            print(e)
            return '', 204
