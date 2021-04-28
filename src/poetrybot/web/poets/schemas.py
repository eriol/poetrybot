from marshmallow import Schema, ValidationError, fields


class PoetSchema(Schema):
    """Schema for poets."""

    id = fields.Int(required=False)
    name = fields.String(required=True)
