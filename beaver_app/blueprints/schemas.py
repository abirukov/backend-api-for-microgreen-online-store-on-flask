from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from beaver_app.db.db import db_session


class BaseSchema(SQLAlchemyAutoSchema):
    class Meta:
        sqla_session = db_session
