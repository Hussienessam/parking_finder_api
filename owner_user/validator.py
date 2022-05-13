from cerberus import Validator

create_garage_schema = {
    'id': {'type': 'string', 'required': True}, 
    'capacity': {'type': 'integer', 'required': True},
    'cameraIDs': { 'type': 'list', 'required': True},
    'location': { 'type': 'list', 'items': [{'type': 'string'}, {'type': 'string'}], 'required': True},
    'ownerID': {'type': 'integer', 'required': True}
}

def validate(document): 
    v = Validator(create_garage_schema)
    return v.validate(document), v.errors