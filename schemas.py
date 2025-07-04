from marshmallow import  Schema, fields

class MessageSchema(Schema):
    message = fields.Str()

class PlianItemSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)
  
class PlainStoreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)

class PlainTagSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)

class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()
    store_id = fields.Int()

class ItemSchema(PlianItemSchema):
    store_id =  fields.Int(required=True, load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
    tags = fields.Nested(PlainTagSchema(), dump_only=True)

class TagSchema(PlainTagSchema):
    store_id =  fields.Int(load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
    items = fields.List(fields.Nested(PlianItemSchema()), dum_only = True)


class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlianItemSchema()), dum_only = True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dum_only = True)

class TagAndItemSchema(Schema):
    message = fields.Str()
    item = fields.Nested(ItemSchema)
    tag = fields.Nested(TagSchema)

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only= True)


class ErrorSchema(Schema):
    code = fields.Integer(required=True)
    status = fields.String(required=True)
    message = fields.String(required=True)

