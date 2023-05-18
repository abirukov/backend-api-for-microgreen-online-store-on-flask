from flask import Flask
from logging.config import dictConfig
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from beaver_app.config import get_config, get_connection_dsn


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
    engine = create_engine(get_connection_dsn(app.config), echo=True, query_cache_size=0)
    scoped_session(sessionmaker(engine))

    return app
