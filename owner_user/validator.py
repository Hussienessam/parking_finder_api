from cerberus import Validator


def built_schema(is_required):
    garage_schema = {
        'id': {'type': 'string', 'required': True},
        'capacity': {'type': 'integer', 'required': is_required},
        'cameraIDs': {'type': 'list', 'required': is_required},
        'location': {'type': 'list', 'items': [{'type': 'string'}, {'type': 'string'}],
                     'required': is_required},
        'ownerID': {'type': 'integer', 'required': is_required}
    }
    return garage_schema


def validate(document, is_required):
    schema = built_schema(is_required)
    v = Validator(schema)
    return v.validate(document), v.errors
