import user.user_app as user_app
from user_operations.HTTP_Exception import HTTP_Exception

def document_validation(db, document, collection):
    if collection == 'Bookmark':
        validate_unique_bookmark(db, document)
    
    if collection == 'Bookmark' or collection == 'Recent' or collection == 'Review':
        validate_driver(db, document)

    if collection == 'Garage':
        validate_owner(db, document)
    
    if collection == 'GarageCamera' or collection == 'Review':
        validate_garage(db, document)

    if collection == "Review":
        validate_review_camera(db, document)

    if collection == "Snaps":
        if(document['mock_garage']):
            validate_garage_camera(db, document)
        else:
            validate_camera(db, document)

def validate_unique_bookmark(db, document):
    if 'driverID' in document:
        bookmark_ref = db.collection('Bookmark')
        bookmark_location = document['location']
        driver_id = document['driverID']
        docs = bookmark_ref.where('driverID', '==', driver_id).stream()
        for doc in docs:
            doc = doc.to_dict()
            if bookmark_location == doc['location']:
                raise HTTP_Exception("Bookmark previously added", 400)

def validate_driver(db, document):
    if 'driverID' in document:
        response = user_app.get_user_by_id(document['driverID'])
        
        if 'id' not in response:
            raise HTTP_Exception("invalid driverID", 400)
            
        if user_app.get_role(document['driverID'], db) != 'driver':
            raise HTTP_Exception('Permission denied', 403)

def validate_owner(db, document):
    if 'ownerID' in document:
        response = user_app.get_user_by_id(document['ownerID'])

        if 'id' not in response :
            raise HTTP_Exception("invalid ownerID", 400)

        if user_app.get_role(document['ownerID'], db) != 'owner':
            raise HTTP_Exception('Permission denied', 403)

def validate_garage(db, document):
    if 'garageID' in document:
        doc_ref = db.collection("Garage")        
        
        if not doc_ref.document(document['garageID']).get().exists:
            raise HTTP_Exception("invalid garageID", 400)
    
def validate_review_camera(db, document):
    if 'cameraID' in document and 'garageID' in document:
        raise HTTP_Exception("invalid review body", 400)
        
    if 'cameraID' in document:
        validate_camera(db, document)

def validate_camera(db, document):
    if 'cameraID' in document:
        doc_ref = db.collection("Camera")        
        if not doc_ref.document(document['cameraID']).get().exists:
            raise HTTP_Exception("invalid cameraID", 400)

def validate_garage_camera(db, document):
    doc_ref = db.collection("GarageCamera")        
    if not doc_ref.document(document['cameraID']).get().exists:
        raise HTTP_Exception("invalid cameraID", 400)