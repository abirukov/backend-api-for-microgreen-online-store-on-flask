import os
from typing import Any, Mapping

from dotenv import load_dotenv

if os.path.exists(os.path.join(os.path.dirname(__file__), '../.env')):
    load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))


def get_config() -> Mapping[str, Any]:
    return {
        'SECRET_KEY': os.environ.get('SECRET_KEY', 'secret_key'),
        'POSTGRES_DBNAME': os.environ.get('POSTGRES_DBNAME'),
        'POSTGRES_HOST': os.environ.get('POSTGRES_HOST', '127.0.0.1'),
        'POSTGRES_PORT': int(os.environ.get('POSTGRES_PORT', 5432)),
        'POSTGRES_USER': os.environ.get('POSTGRES_USER', 'postgres'),
        'POSTGRES_PASSWORD': os.environ.get('POSTGRES_PASSWORD', ''),
        'SQLALCHEMY_TRACK_MODIFICATIONS': os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS', False),
        'API_TITLE': 'Green Beaver API',
        'API_VERSION': 'v1',
        'OPENAPI_VERSION': '3.0.2',
        'TOKEN_LIFETIME_IN_HOURS': int(os.environ.get('TOKEN_LIFETIME_IN_HOURS', 24)),
    }


def get_connection_dsn(config: Mapping[str, Any]) -> str:
    return (
        f'postgresql://{config["POSTGRES_USER"]}:{config["POSTGRES_PASSWORD"]}@'
        f'{config["POSTGRES_HOST"]}:{config["POSTGRES_PORT"]}/{config["POSTGRES_DBNAME"]}'
    )
