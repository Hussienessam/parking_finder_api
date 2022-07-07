import user.user_app as user_app

def document_validation(db, document, collection):
    validated = True
    error = ""
    if collection == 'Bookmark':
        validated, error = validate_unique_bookmark(db, document)
        if not validated:
            return validated, error
    
    if collection == 'Bookmark' or collection == 'Recent' or collection == 'Review':
        validated, error = validate_driver(db, document)
        if not validated:
            return validated, error

    if collection == 'Garage':
        validated, error = validate_owner(db, document)
        if not validated:
            return validated, error
    
    if collection == 'GarageCamera' or collection == 'Review':
        validated, error = validate_garage(db, document)
        if not validated:
            return validated, error

    if collection == "Review":
        validated, error = validate_review_camera(db, document)
        if not validated:
            return validated, error

    if collection == "Snaps":
        validated, error = validate_camera(db, document)
        if not validated:
            return validated, error

    if collection == "GarageSnaps":
        validated, error = validate_garage_camera_for_collection(db, document)
        if not validated:
            return validated, error
    
    return validated, error


def validate_unique_bookmark(db, document):
    try:
        if 'driverID' not in document:
            return True, ""

        bookmark_ref = db.collection('Bookmark')
        bookmark_location = document['location']
        driver_id = document['driverID']
        docs = bookmark_ref.where('driverID', '==', driver_id).stream()
        for doc in docs:
            doc = doc.to_dict()
            if(bookmark_location == doc['location']):
                return False, "Bookmark previously added"
        return True, ""
    except Exception as e:
        return False, f"An Error Occurred: {e}"

def validate_driver(db, document):
    try:
        if 'driverID' not in document:
            return True, ""

        response = user_app.get_user_by_id(document['driverID'])

        if 'id' not in response or user_app.get_role(document['driverID'], db) != 'driver':
            return False, "invalid driverID"

        return True, ""
            
    except Exception as e:
        return False, f"An Error Occurred: {e}"

def validate_owner(db, document):
    try:
        if 'ownerID' not in document:
            return True, ""

        response = user_app.get_user_by_id(document['ownerID'])

        if 'id' not in response or user_app.get_role(document['ownerID'], db) != 'owner':
            return False, "invalid ownerID"
        return True, ""
            
    except Exception as e:
        return False, f"An Error Occurred: {e}"

def validate_garage(db, document):
    try:
        if 'garageID' not in document or document['garageID'] == '':
                return True, ""

        doc_ref = db.collection("Garage")        
        if doc_ref.document(document['garageID']).get().exists:
            return True, ""

        else:
            return False, "invalid garageID"
    except Exception as e:
        return False, f"An Error Occurred: {e}"

def validate_garage_camera(db, document):
    doc_ref = db.collection("Garage")
    garage_doc = doc_ref.document(document['garageID']).get().to_dict()
    if document['cameraID'] in garage_doc['cameraIDs']:
        return True, ""
    else:
        return False, "Garage does not contain given cameraID"
    
def validate_review_camera(db, document):
    if 'cameraID' not in document:
            return True, ""

    validated = True
    error = "" 

    if document['garageID'] == '':
        validated, error = validate_camera(db, document)
    else:
        validated, error = validate_garage_camera(db, document)

    if validated:
        return True, "" 
    else:
        return validated, error
    

def validate_camera(db, document):
    try:
        if 'cameraID' not in document:
                return True, ""
        
        doc_ref = db.collection("Camera")        
        if doc_ref.document(document['cameraID']).get().exists:
            return True, ""

        else:
            return False, "invalid cameraID"
    except Exception as e:
        return False, f"An Error Occurred: {e}"

def validate_garage_camera_for_collection(db, document):
    try:
        if 'garageCameraID' not in document:
                return True, ""

        doc_ref = db.collection("GarageCamera")        
        if doc_ref.document(document['garageCameraID']).get().exists:
            return True, ""

        else:
            return False, "invalid garageCameraID"
    except Exception as e:
        return False, f"An Error Occurred: {e}"