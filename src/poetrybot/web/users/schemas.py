from marshmallow import Schema, fields, ValidationError


def validate_id(n):
    """Validate the id field."""
    # https://core.telegram.org/bots/api#chat
    # We use an heuristic approach here, it seems that at least
    if n < 100000:
        raise ValidationError("id must be greater than 99999.")


class UserSchema(Schema):
    id = fields.Int(validate=validate_id, required=True)
    name = fields.String(required=True)
