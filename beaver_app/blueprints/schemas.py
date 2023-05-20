import marshmallow as ma

class ProductSchema(ma.Schema):
    id = ma.fields.UUID(dump_only=True)
    title = ma.fields.String()
    price = ma.fields.Float()
    description = ma.fields.String()
    category_id = ma.fields.UUID()
    category = ma.fields.Nested(lambda: CategorySchema())


class CategorySchema(ma.Schema):
    id = ma.fields.UUID(dump_only=True)
    title = ma.fields.String()
    products = ma.fields.List(ma.fields.Nested(ProductSchema(exclude=("category",))))
