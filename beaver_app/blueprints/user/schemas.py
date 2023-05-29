from beaver_app.blueprints.schemas import BaseSchema
from beaver_app.blueprints.user.models.user import User


class UserSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = User
        include_relationships = True
        load_instance = True
        include_fk = True
