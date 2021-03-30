from marshmallow import Schema, fields, ValidationError


class PoetSchema(Schema):
    """Schema for poets."""

    id = fields.Int(required=False)
    name = fields.String(required=True)
