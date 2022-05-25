from cerberus import Validator
import user_operations.user_queries_app as user_queries

def built_schema(collection, is_required):
    camera_schema = {
        'id': {'type': 'string', 'required': True},
        'address': {'type': 'string', 'required': is_required},
        'location': {'type': 'dict', 'schema': {'lat': {'type': 'string', 'required': is_required},
                                                'long': {'type': 'string', 'required': is_required}}, 
                                                'required': is_required},
    }

    garage_schema = {
        'id': {'type': 'string', 'required': True},
        'capacity': {'type': 'integer', 'required': is_required},
        'address': {'type': 'string', 'required': is_required},
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

    if collection == "Camera":
        return camera_schema

    elif collection == "Garage":
        return garage_schema

    elif collection == "Review":
        return review_schema
        
    elif collection == "Bookmark":
        return bookmark_schema

def unique_validation(db, document, collection):
    if collection == "Bookmark":
        is_unique = user_queries.validate_unique_bookmark(db, document)
        if is_unique:
            return True, ""
        else:
            return False, "Bookmark previously added"

def validate(db, document, collection, is_required):
    schema = built_schema(collection, is_required)
    v = Validator(schema)
    validated = v.validate(document)
    if validated:
        unique_validated, error = unique_validation(db, document, collection)
        return unique_validated, error
    else:
        return validated, v.errors