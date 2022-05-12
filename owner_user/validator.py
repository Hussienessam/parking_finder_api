from cerberus import Validator

garage_schema = {
    'id': {'type': 'string', 'required': True}, 
    'capacity': {'type': 'integer', 'required': True},
    'cameraIDs': { 'type': 'list', 'required': True},
    'location': { 'type': 'list', 'items': [{'type': 'string'}, {'type': 'string'}], 'required': True},
    'ownerID': {'type': 'integer', 'required': True}
}

# document = {
#     'id': 'john doe',
#     'capacity': 3,
#     'cameraIDs': ['0','1'],
#     'location': ['de', 'do'],
#     'ownerID': 2
# }

def validate(document): 
    
    v = Validator(garage_schema)
    return v.validate(document), v.errors