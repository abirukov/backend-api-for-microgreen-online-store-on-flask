import sentry_sdk

from flask import Flask
from flask_smorest import Api
from logging.config import dictConfig
from sentry_sdk.integrations.flask import FlaskIntegration

from beaver_app.blueprints.category.routes import category_blueprint
from beaver_app.blueprints.product.routes import product_blueprint
from beaver_app.config import get_config


def create_app() -> Flask:

    sentry_sdk.init(
        dsn="https://46ba4ee456734c1e88da5ba1b320ad18@o1164730.ingest.sentry.io/4505240675942400",
        integrations=[
            FlaskIntegration(),
        ],

        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=1.0
    )

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
