import marshmallow as ma


class CategorySchema(ma.Schema):
    id = ma.fields.UUID(dump_only=True)
    title = ma.fields.String()
