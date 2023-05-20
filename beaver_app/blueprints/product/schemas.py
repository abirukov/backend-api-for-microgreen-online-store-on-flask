import marshmallow as ma


class ProductSchema(ma.Schema):
    id = ma.fields.UUID(dump_only=True)
    title = ma.fields.String()
    price = ma.fields.Float()
    description = ma.fields.String()
    category_id = ma.fields.UUID()
