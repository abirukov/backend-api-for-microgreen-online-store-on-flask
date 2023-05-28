from typing import Any, Mapping

from beaver_app.config import get_connection_dsn


def test__get_connection_dsn(config: Mapping[str, Any]) -> None:
    assert get_connection_dsn(config) == 'postgresql://postgres:devpass@localhost:5432/postgres'
