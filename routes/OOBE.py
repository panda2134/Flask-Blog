from sqlalchemy.exc import ProgrammingError


from utils import Option
from flask_restful import reqparse, Resource


class OOBE(Resource):
    @staticmethod
    def get():
        try:
            Option.get_option('site.title')
            return 'gone', 410
        except ProgrammingError as e: # database not set up properly, ok to do OOBE
            return '', 204

    @staticmethod
    def post():
        try:
            Option.get_option('site.title')
            return 'gone', 410
        except ProgrammingError as e: # database not set up properly, ok to do OOBE
            # check for request
            parser = reqparse.RequestParser()
            parser.add_argument('blogMeta', required=True)
            # set up database
            from models import db
            db.create_all()

