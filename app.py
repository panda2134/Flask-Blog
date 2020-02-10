from connexion import FlaskApp
from connexion.resolver import MethodViewResolver
from flask_cors import CORS
import views
import models


def create_app():
    con = FlaskApp(__name__, specification_dir='vue-blog-api')
    # con.add_api('api.yaml', resolver=MethodViewResolver('views'), validate_responses=True)
    con.add_api('api.yaml', resolver=MethodViewResolver('views'))

    app = con.app
    app.config.from_pyfile('config.py')
    models.init_app(app)
    CORS(app, resources='/api/*', supports_credentials=True)

    return app


if __name__ == '__main__':
    create_app().run()
