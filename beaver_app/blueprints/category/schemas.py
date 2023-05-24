from beaver_app.blueprints.category.models import Category
from beaver_app.blueprints.schemas import BaseSchema


class CategorySchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = Category
        include_relationships = True
        load_instance = True
