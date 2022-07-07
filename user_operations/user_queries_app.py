from flask import request, jsonify
from firebase_admin import firestore
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
            doc['cameraID'] = get_garage_camera(doc['cameraID'], db)
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
                doc['cameraIDs'][i] = get_garage_camera(doc['cameraIDs'][i],db)
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
        return jsonify(response), 200
    except Exception as e:
        return f"An Error Occurred: {e}", 400


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