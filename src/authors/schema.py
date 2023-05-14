from marshmallow import Schema, fields, validate


class AuthorSchema(Schema):
    name = fields.Str(required=True)