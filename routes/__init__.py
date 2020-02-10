from .OOBE import OOBE
from flask_restful import Api

api = Api(prefix='/api/v1')

api.add_resource(OOBE, '/oobe')


def init_app(app):
    api.init_app(app)
