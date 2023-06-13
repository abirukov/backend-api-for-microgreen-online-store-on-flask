from beaver_app.db.db import Base


class BaseModel(Base):
    @staticmethod
    def get_search_fields() -> list:
        return []
