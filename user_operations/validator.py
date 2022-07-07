from cerberus import Validator
import user_operations.user_validations_app as user_validations

def built_schema(collection, is_required):
    camera_schema = {
        'id': {'type': 'string', 'required': True},
        'address': {'type': 'string', 'required': is_required},
        'location': {'type': 'dict', 'schema': {'lat': {'type': 'string', 'required': is_required},
                                                'long': {'type': 'string', 'required': is_required}}, 
                                                'required': is_required},
    }

    garage_camera_schema = {
        'id': {'type': 'string', 'required': True},
        'address': {'type': 'string', 'required': is_required},
        'garageID': {'type': 'string', 'required': is_required}
    }

    garage_schema = {
        'id': {'type': 'string', 'required': True},
        'capacity': {'type': 'string', 'required': is_required},
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
        'locationURL' : {'type': 'string', 'required': is_required},
        'location': {'type': 'dict', 'schema': {'lat': {'type': 'string', 'required': is_required},
                                                'long': {'type': 'string', 'required': is_required}}, 
                                                'required': is_required}
    }

    recent_schema = {
        'driverID': {'type': 'string', 'required': is_required},
        'recent': {'type': 'dict', 'required': is_required}
    }

    snap_schema = {
        'cameraID': {'type': 'string', 'required': True},
        'capacity': {'type': 'string', 'required': is_required},
        'path': {'type': 'string', 'required': is_required},
        'mock_garage': {'type': 'boolean', 'required': is_required}
    }

    if collection == "Camera":
        return camera_schema

    elif collection == "GarageCamera":
        return garage_camera_schema

    elif collection == "Garage":
        return garage_schema

    elif collection == "Review":
        return review_schema
        
    elif collection == "Bookmark":
        return bookmark_schema
    
    elif collection == "Snaps" or collection == "GarageSnaps":
        return snap_schema

    elif collection == "Recent":
        return recent_schema


def validate(db, document, collection, is_required):
    schema = built_schema(collection, is_required)
    v = Validator(schema)
    validated = v.validate(document)

    if validated:
        document_validated, error = user_validations.document_validation(db, document, collection)
        return document_validated, error
    else:
        return validated, v.errors