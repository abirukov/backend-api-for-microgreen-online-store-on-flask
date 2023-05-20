from flask import Flask
from logging.config import dictConfig

from flask_smorest import Api

from beaver_app.blueprints.category.routes import category_blueprint
from beaver_app.blueprints.product.routes import product_blueprint
from beaver_app.config import get_config


def create_app() -> Flask:

    dictConfig({
        'version': 1,
        'formatters': {'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }},
        'handlers': {'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default',
        }},
        'root': {
            'level': 'INFO',
            'handlers': ['wsgi'],
        },
    })
    app = Flask(__name__)
    app.config.update(get_config())
    api = Api(app)
    api.register_blueprint(product_blueprint)
    api.register_blueprint(category_blueprint)
    return app
