from beaver_app.db.db import Base
from abc import ABC


class BaseModel(ABC, Base):
    @staticmethod
    def get_search_fields() -> list:
        return []
