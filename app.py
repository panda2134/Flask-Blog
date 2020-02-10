from flask import Flask
import routes
import models


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    routes.init_app(app)
    models.init_app(app)

    return app


if __name__ == '__main__':
    create_app().run()
