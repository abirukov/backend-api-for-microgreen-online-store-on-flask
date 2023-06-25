from flask import Flask
from flask_jwt_extended import JWTManager
from flask_smorest import Api
from logging.config import dictConfig

from beaver_app.blueprints.basket.routes import basket_blueprint
from beaver_app.blueprints.category.routes import category_blueprint
from beaver_app.blueprints.product.routes import product_blueprint
from beaver_app.blueprints.order.routes import order_blueprint
from beaver_app.blueprints.user.models import TokenBlocklist
from beaver_app.blueprints.user.routes import user_blueprint
from beaver_app.config import get_config
from beaver_app.db.db import db_session


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
    api.register_blueprint(user_blueprint)
    api.register_blueprint(basket_blueprint)
    api.register_blueprint(order_blueprint)
    jwt_manager = JWTManager(app)

    @jwt_manager.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:  # noqa: U100
        jti = jwt_payload['jti']
        token = db_session.query(TokenBlocklist.id).filter_by(jti=jti).first()

        return token is not None

    return app
