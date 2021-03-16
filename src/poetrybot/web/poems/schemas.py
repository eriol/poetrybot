from marshmallow import Schema, fields


class PoemSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.String()
    verses = fields.String(required=True)
    poet_id = fields.Int(required=True)
