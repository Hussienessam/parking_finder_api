from cerberus import Validator

def built_schema(required):
    garage_schema = {
        'id': {'type': 'string', 'required': True}, 
        'capacity': {'type': 'integer', 'required': bool(required)},
        'cameraIDs': { 'type': 'list', 'required': bool(required)},
        'location': { 'type': 'list', 'items': [{'type': 'string'}, {'type': 'string'}],
         'required': bool(required)},
        'ownerID': {'type': 'integer', 'required': bool(required)}
    }
    return garage_schema

def validate(document, required): 
    schema = built_schema(required)
    v = Validator(schema)
    return v.validate(document), v.errors