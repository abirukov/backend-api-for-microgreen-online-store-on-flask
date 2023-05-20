from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base

from beaver_app.config import get_connection_dsn, get_config

db = SQLAlchemy()
engine = create_engine(get_connection_dsn(get_config()), echo=True, query_cache_size=0)
db_session = scoped_session(sessionmaker(engine))

Base = declarative_base()
Base.query = db_session.query_property()
