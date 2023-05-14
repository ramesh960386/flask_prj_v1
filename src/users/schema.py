from marshmallow import Schema, fields, validate


class SignupSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=4))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6))
    role = fields.Str()
        

class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6))