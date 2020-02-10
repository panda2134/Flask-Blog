from .OOBE import OOBE
from flask_restful import Api

api = Api()

api.add_resource(OOBE, '/oobe')
