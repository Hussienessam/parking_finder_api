from flask import request, jsonify
from firebase_admin import firestore
from regex import F
import user_operations.user_operations_app as user_operations
import user.user_app as user_app
import datetime as dt

def show_garage_reviews(db):
    try:
        review_ref = db.collection('Review')
        garage_id = request.args.get('garageID')
        reviews = review_ref.where('garageID', '==', garage_id).order_by('date', direction=firestore.Query.DESCENDING).stream()
        response = []
        for doc in reviews:
            doc = doc.to_dict()
            doc['cameraID'] = user_operations.get_camera(doc['cameraID'], db)
            doc['driverID'] = user_app.get_by_id_for_garage(doc['driverID'])
            response.append(doc)
        return jsonify(response), 200
    except Exception as e:
        return f"An Error Occurred: {e}", 400


def show_street_reviews(db):
    try:
        review_ref = db.collection('Review')
        camera_id = request.args.get('cameraID')
        reviews = review_ref.where('cameraID', '==', camera_id).order_by('date', direction=firestore.Query.DESCENDING).stream()
        result = [review.to_dict() for review in reviews]
        return jsonify(result), 200
    except Exception as e:
        return f"An Error Occurred: {e}", 400


def get_owner_garages(db):
    try:
        garage_ref = db.collection('Garage')
        ownerID = request.args.get('ownerID')
        docs = garage_ref.where('ownerID', '==', ownerID).stream()
        response = []
        for doc in docs:
            doc = doc.to_dict()
            for i in range(len(doc['cameraIDs'])):
                doc['cameraIDs'][i] = user_operations.get_camera(doc['cameraIDs'][i],db)
            response.append(doc)
        return jsonify(response), 200
    except Exception as e:
        return f"An Error Occurred: {e}", 400

def get_user_bookmark(db):
    try:
        bookmark_ref = db.collection('Bookmark')
        driverID = request.args.get('driverID')
        docs = bookmark_ref.where('driverID', '==', driverID).stream()
        response = [doc.to_dict() for doc in docs]
        return jsonify(response), 200
    except Exception as e:
        return f"An Error Occurred: {e}", 400

def validate_unique_bookmark(db, document):
    try:
        bookmark_ref = db.collection('Bookmark')
        bookmark_location = document['location']
        driver_id = document['driverID']
        docs = bookmark_ref.where('driverID', '==', driver_id).stream()
        for doc in docs:
            doc = doc.to_dict()
            if(bookmark_location == doc['location']):
                return False
        return True
    except Exception as e:
        return f"An Error Occurred: {e}", 400

def handle_delete(db, collection_ref, doc):
    if collection_ref == 'Garage':
        camera_ref = db.collection('GarageCamera')
        doc = doc.to_dict()
        for i in range(len(doc['cameraIDs'])):
            camera_ref.document(doc['cameraIDs'][i]).delete()
    
    if collection_ref == 'GarageCamera':
        doc = doc.to_dict()
        doc_id = doc['id']
        garage_ref = db.collection('Garage')
        garages = garage_ref.where('cameraIDs', 'array_contains', doc_id).stream()
        for garage in garages:
            garage = garage.to_dict()
            for i in range(len(garage['cameraIDs'])):
                if garage['cameraIDs'][i] == doc_id:
                    garage['cameraIDs'].pop(i)
                    garage_ref.document(garage['id']).update(garage)
                    break

def handle_add(db, collection_ref, doc):
    if collection_ref == 'GarageCamera':
        garage_ref = db.collection("Garage")
        garage_doc = garage_ref.document(doc['garage_id']).get().to_dict()
        garage_doc['cameraIDs'].append(doc['id'])
        garage_ref.document(doc['garage_id']).update(garage_doc)

def handle_driver_history(collection_ref, db, doc):
    try:
        doc_ref = db.collection(collection_ref)
        if doc_ref.document(doc['driverID']).get().exists:
            recent_doc = doc_ref.document(doc['driverID']).get().to_dict()
            recent_doc['history'].append({'recent': doc['recent']})
            doc_ref.document(doc['driverID']).update(recent_doc)
        else:
            new_doc = {'driverID': doc['driverID'], 'history': [{'recent': doc['recent']}]}
            doc_ref.document(doc['driverID']).set(new_doc)

        return jsonify("success"), 200
    except Exception as e:
        return f"An Error Occurred: {e}", 400

def clear_driver_history(db):
    try:
        doc_ref = db.collection('Recent')
        driverID = request.args.get('driverID')

        if doc_ref.document(driverID).get().exists:
            doc_ref.document(driverID).delete()
            return jsonify("History is cleared successfully"), 200

        else:
            return "driver doesn't have history yet", 404
    
    except Exception as e:
        return f"An Error Occurred: {e}", 400

def clear_driver_bookmark(db):
    try:
        doc_ref = db.collection('Bookmark')
        driverID = request.args.get('driverID')
        docs = doc_ref.where('driverID', '==', driverID).stream()
        empty = True
        
        for doc in docs:
            doc = doc.to_dict()
            doc_ref.document(doc['id']).delete()
            empty = False

        if empty:
            return "driver doesn't have bookmarks yet", 404
        return jsonify("Bookmarks are cleared successfully"), 200
    
    except Exception as e:
        return f"An Error Occurred: {e}", 400

def get_camera_info(db):
    try:
        garage_ref = db.collection('Garage')
        camera_ref = db.collection('GarageCamera')
        cameraID = request.args.get('cameraID')
        if camera_ref.document(cameraID).get().exists:
            docs = garage_ref.where('cameraIDs', 'array_contains', cameraID).stream()
            for doc in docs:
                doc = doc.to_dict()
                response = {'location': doc['location'], 'address': doc['address']}
            return jsonify(response), 200
        else:
            return "Camera doesn't exist", 404
    except Exception as e:
        return f"An Error Occurred: {e}", 400
        
def get_ordered_reviews(db):
    try:
        review_ref = db.collection('Review')
        docs = review_ref.order_by('date', direction=firestore.Query.DESCENDING).stream()
        response = [doc.to_dict() for doc in docs]
        return response
    except Exception as e:
        return f"An Error Occurred: {e}", 400


def update_snaps(db, snap, mock_garage):
    try:
        if mock_garage :
            collection_ref = db.collection('GarageSnaps')
            docs = collection_ref.where('garageCameraID', '==', snap['cameraID']).stream()
        else :
            collection_ref = db.collection('Snaps')
            docs = collection_ref.where('cameraID', '==', snap['cameraID']).stream()
        response = [doc.to_dict() for doc in docs]

        if len(response) == 0:
            doc_ref = collection_ref.document()
            doc = {'id': doc_ref.id, 'date': dt.datetime.now(),
             'capacity': snap['capacity'], 'path': snap['path']}
            
            if mock_garage:
                doc.update({'garageCameraID': snap['cameraID']})
            else:
                doc.update({'cameraID': snap['cameraID']})
            
            doc_ref.set(doc)
            return jsonify(f"Document is added successfully"), 200

        else:
            collection_ref.document(response[0]['id']).update({'date': dt.datetime.now(), 
            'path': snap['path']})
            return jsonify("Document is updated successfully"), 200

    except Exception as e:
        return f"An Error Occurred: {e}", 400