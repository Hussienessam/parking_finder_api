from user_operations.HTTP_Exception import HTTP_Exception
import user.user_app as user_app

def authorize_request(collection, db, request, userID):
    if user_app.get_role(userID, db) == "admin":
        return    

    if collection == 'Camera' or collection == 'Snaps' and request.method == "GET":
        return
    
    change_request = False

    if request.method == "PUT" and 'driverID' in request.json  or request.method == "POST":
        change_request = True

    if collection == "Bookmark" or collection == "Review" or collection == "DriverRequests" or collection == "Recent":
        authorize_driver(collection, db, request, userID, change_request)


    elif collection == "Garage":
        authorize_owner(collection, db, request, userID, change_request)
    
    elif collection == "GarageSnaps" or collection == "GarageCamera" or collection == "CameraRequest":
        authorize_garage_owner(collection, db, request, userID, change_request)
    
    elif collection == "OwnerRequest":
        if userID != request.args.get('id'):
            raise HTTP_Exception('Permission denied', 403) 
            
    else:
        raise HTTP_Exception('Permission denied', 403) 

def authorize_driver(collection, db, request, userID, change_request):
    if collection == "DriverRequests":
        driverID = request.args.get('driverID')
        if not driverID:
            driverID = request.json['driverID']

        if driverID != userID:
            raise HTTP_Exception('Permission denied', 403) 

    else:
        if change_request:
            if request.json['driverID'] != userID:
                raise HTTP_Exception('Permission denied', 403)     
    
        else:
            id = request.args.get('id')
            if not db.collection(collection).document(id).get().exists:
                raise HTTP_Exception("document doesn't exit", 404)
        
            doc = db.collection(collection).document(id).get().to_dict()
            if doc['driverID'] != userID:
                raise HTTP_Exception('Permission denied', 403) 

def authorize_owner(collection, db, request, userID, change_request):
    if change_request:
        if request.json['ownerID'] != userID:
            raise HTTP_Exception('Permission denied', 403)
    
    else:
        id = request.args.get('id')
        if not db.collection(collection).document(id).get().exists:
            raise HTTP_Exception("document doesn't exit", 404)

        doc = db.collection(collection).document(id).get().to_dict()
        if doc['ownerID'] != userID:
            raise HTTP_Exception('Permission denied', 403)
        
def authorize_user(request, userID):
    user_id = request.json['id']
    
    if user_id != userID:
        raise HTTP_Exception('Permission denied', 403)

def authorize_garage_owner(collection, db, request, userID, change_request):
    if change_request:
        garage_id = request.json['garageID']

    else:
        id = request.args.get('id')
        if collection == 'CameraRequest':
            id = request.args.get('cameraID')

        if not db.collection('GarageCamera').document(id).get().exists:
            raise HTTP_Exception("document doesn't exit", 404)
        
        garage_camera_doc = db.collection('GarageCamera').document(id).get().to_dict()
        garage_id = garage_camera_doc['garageID']

    garage_doc = db.collection('Garage').document(garage_id).get().to_dict()

    if garage_doc['ownerID'] != userID:
        raise HTTP_Exception('Permission denied', 403)