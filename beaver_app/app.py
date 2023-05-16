import logging

from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from beaver_app.config import get_config, get_connection_dsn
logging.basicConfig(level=logging.INFO)


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.update(get_config())
    app.engine = create_engine(get_connection_dsn(app.config), echo=True, query_cache_size=0)
    app.session = scoped_session(sessionmaker(app.engine))

    return app
