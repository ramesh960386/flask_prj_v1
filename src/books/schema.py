from marshmallow import Schema, fields, validate


class BookSchema(Schema):
    title = fields.Str(required=True)
    author_id = fields.Int(required=True)
    year_published = fields.Int(required=True)
    params = fields.Dict()