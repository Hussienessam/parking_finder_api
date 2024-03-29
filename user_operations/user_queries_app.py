from flask import request, jsonify
from firebase_admin import firestore
import user.user_app as user_app
import datetime as dt
from user_operations.HTTP_Exception import HTTP_Exception

def show_garage_reviews(db):
    try:
        review_ref = db.collection('Review')
        garage_id = request.args.get('garageID')
        reviews = review_ref.where('garageID', '==', garage_id).order_by('date', direction=firestore.Query.DESCENDING).stream()
        response = []
        for doc in reviews:
            doc = doc.to_dict()
            doc['driverID'] = user_app.get_user_by_id(doc['driverID'])
            response.append(doc)
        return jsonify(response), 200

    except Exception as e:
        return f"An Error Occurred: {e}", 400


def show_street_reviews(db):
    try:
        review_ref = db.collection('Review')
        camera_id = request.args.get('cameraID')
        reviews = review_ref.where('cameraID', '==', camera_id).order_by('date', direction=firestore.Query.DESCENDING).stream()
        response = []
        for doc in reviews:
            doc = doc.to_dict()
            doc['driverID'] = user_app.get_user_by_id(doc['driverID'])
        return jsonify(response), 200
    except Exception as e:
        return f"An Error Occurred: {e}", 400


def get_owner_garages(db):
    garage_ref = db.collection('Garage')
    ownerID = request.args.get('ownerID')
    docs = garage_ref.where('ownerID', '==', ownerID).stream()
    response = []
    for doc in docs:
        doc = doc.to_dict()
        for i in range(len(doc['cameraIDs'])):
            doc['cameraIDs'][i] = get_garage_camera(doc['cameraIDs'][i],db)
        response.append(doc)
    return jsonify(response), 200

def get_user_bookmark(db):
    bookmark_ref = db.collection('Bookmark')
    driverID = request.args.get('driverID')
    docs = bookmark_ref.where('driverID', '==', driverID).stream()
    response = [doc.to_dict() for doc in docs]
    return jsonify(response), 200


def get_location_bookmark(db):
    bookmark_ref = db.collection('Bookmark')
    driverID = request.json['driverID']
    
    docs = bookmark_ref.where('driverID', '==', driverID).stream()
    bookmarks = [doc.to_dict() for doc in docs]

    if len(bookmarks) == 0:
        return jsonify(), 200
    
    else:
        for doc in bookmarks:
            if doc['location'] == request.json['location']:
                return jsonify(doc), 200
            return jsonify(), 200

def get_garage_camera(id, db):
    try:
        doc_ref = db.collection("GarageCamera")
        doc_id = id
        if doc_id:
            if doc_ref.document(doc_id).get().exists:
                doc = doc_ref.document(doc_id).get()
                return doc.to_dict()
            else:
                return "document doesn't exist", 404
        else:
            all_docs = [doc.to_dict() for doc in doc_ref.stream()]
            return jsonify(all_docs), 200

    except Exception as e:
        return f"An Error Occurred: {e}", 400

def clear_driver_history(db):
    doc_ref = db.collection('Recent')
    driverID = request.args.get('driverID')

    doc_ref.document(driverID).update({'history': []})
    return jsonify("History is cleared successfully"), 200
        

def clear_driver_bookmark(db):
    doc_ref = db.collection('Bookmark')
    driverID = request.args.get('driverID')
    docs = doc_ref.where('driverID', '==', driverID).stream()
    
    for doc in docs:
        doc = doc.to_dict()
        doc_ref.document(doc['id']).delete()

    return jsonify("Bookmarks are cleared successfully"), 200


def get_camera_info(db):
    garage_ref = db.collection('Garage')
    camera_ref = db.collection('GarageCamera')
    cameraID = request.args.get('cameraID')
    
    if not camera_ref.document(cameraID).get().exists:
        raise HTTP_Exception("Camera doesn't exist", 404)
    
    docs = garage_ref.where('cameraIDs', 'array_contains', cameraID).stream()
    for doc in docs:
        doc = doc.to_dict()
        response = {'location': doc['location'], 'address': doc['address']}
    
    return jsonify(response), 200
        
        
def get_ordered_reviews(db):
    review_ref = db.collection('Review')
    docs = review_ref.order_by('date', direction=firestore.Query.DESCENDING).stream()
    
    response = [doc.to_dict() for doc in docs]
    return jsonify(response), 200


def update_snaps(db, snap, mock_garage):
    try:
        if mock_garage :
            collection_ref = db.collection('GarageSnaps')
        else :
            collection_ref = db.collection('Snaps')

        if not collection_ref.document(snap['cameraID']).get().exists:
            doc = {'date': dt.datetime.now(),
             'capacity': snap['capacity'], 'path': snap['path']}
            
            if mock_garage:
                doc.update({'garageCameraID': snap['cameraID']})
            else:
                doc.update({'cameraID': snap['cameraID']})
            
            collection_ref.document(snap['cameraID']).set(doc)
            return jsonify(f"Document is added successfully"), 200

        else:
            collection_ref.document(snap['cameraID']).update({'date': dt.datetime.now(), 
            'path': snap['path']})
            return jsonify("Document is updated successfully"), 200

    except Exception as e:
        return f"An Error Occurred: {e}", 400