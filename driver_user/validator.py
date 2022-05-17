from cerberus import Validator

review_schema = {
    "id": {'type': 'string', 'required': True},
    "content": {'type': 'string', 'required': True},
    "date": {'type': 'datetime', 'required': True},
    "cameraID": {'type': 'string', 'required': True},
    'driverID': {'type': 'string', 'required': True},
    'garageID': {'type': 'string', 'required': True}
}

bookmark_schema = {
    "id": {'type': 'string', 'required': True},
    "name": {'type': 'string', 'required': True},
    'driverID': {'type': 'string', 'required': True},
    'location': {'type': 'dict', 'schema': {'lat': {'type': 'string', 'required': True},
                                            'long': {'type': 'string', 'required': True}}}
}


def validate(schema, document):
    v = Validator(schema)
    return v.validate(document), v.errors
