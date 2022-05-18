from cerberus import Validator


def built_schema(collection, is_required):
    garage_schema = {
        'id': {'type': 'string', 'required': True},
        'capacity': {'type': 'integer', 'required': is_required},
        'cameraIDs': {'type': 'list', 'required': is_required},
        'location': {'type': 'dict', 'schema': {'lat': {'type': 'string', 'required': is_required},
                                                'long': {'type': 'string', 'required': is_required}}, 
                                                'required': is_required},
        'ownerID': {'type': 'string', 'required': is_required}
    }

    review_schema = {
        "id": {'type': 'string', 'required': True},
        "content": {'type': 'string', 'required': is_required},
        "date": {'type': 'datetime', 'required': is_required},
        "cameraID": {'type': 'string', 'required': is_required},
        'driverID': {'type': 'string', 'required': is_required},
        'garageID': {'type': 'string', 'required': is_required}
    }

    bookmark_schema = {
        "id": {'type': 'string', 'required': True},
        "name": {'type': 'string', 'required': is_required},
        'driverID': {'type': 'string', 'required': is_required},
        'location': {'type': 'dict', 'schema': {'lat': {'type': 'string', 'required': is_required},
                                                'long': {'type': 'string', 'required': is_required}}, 
                                                'required': is_required}
    }

    if collection == "Garage":
        return garage_schema

    elif collection == "Review":
        return review_schema
        
    elif collection == "Bookmark":
        return bookmark_schema


def validate(document, collection, is_required):
    schema = built_schema(collection, is_required)
    v = Validator(schema)
    return v.validate(document), v.errors
