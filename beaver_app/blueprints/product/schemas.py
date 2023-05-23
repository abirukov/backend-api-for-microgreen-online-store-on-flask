from marshmallow_sqlalchemy import fields

from beaver_app.blueprints.category.schemas import CategorySchema
from beaver_app.blueprints.product.models import Product
from beaver_app.blueprints.schemas import BaseSchema


class ProductSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = Product
        include_relationships = True
        load_instance = True
        include_fk = True
