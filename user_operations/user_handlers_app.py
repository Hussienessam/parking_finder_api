from flask import jsonify
import user_operations.user_queries_app as user_queries
import user_operations.user_auth_app as user_auth
import user_operations.validator as validator

def handle_delete(db, collection_ref, doc):
    doc = doc.to_dict()
    if collection_ref == 'Garage':
        handle_delete_garage_for_cameras(db, doc) 
        handle_delete_garage_for_reviews(db, doc) 

    if collection_ref == 'GarageCamera':
        handle_delete_garage_camera_for_garages(db, doc)        

    if collection_ref == 'Camera' or collection_ref == 'GarageCamera':
        handle_delete_camera_for_reviews(db, doc)
        handle_delete_camera_for_snaps(db, doc, collection_ref)

def handle_delete_garage_camera_for_garages(db, doc):
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

def handle_delete_camera_for_snaps(db, document, collection_ref):
    if collection_ref == "GarageCamera":
        collection = 'GarageSnaps'
    else:
        collection = 'Snaps'
    db.collection(collection).document(document['id']).delete()

def handle_delete_garage_for_cameras(db, doc):
    camera_ref = db.collection('GarageCamera')
    for i in range(len(doc['cameraIDs'])):
        camera_ref.document(doc['cameraIDs'][i]).delete()

def handle_delete_garage_for_reviews(db, document):
    collection_ref = db.collection('Review')
    docs = collection_ref.where('garageID', '==', document['id']).stream()
    for doc in docs:
        doc = doc.to_dict()
        collection_ref.document(doc['id']).delete()

def handle_delete_camera_for_reviews(db, document):
    collection_ref = db.collection('Review')
    docs = collection_ref.where('cameraID', '==', document['id']).stream()
    for doc in docs:
        doc = doc.to_dict()
        collection_ref.document(doc['id']).delete()

def handle_add(db, collection_ref, doc):
    if collection_ref == 'GarageCamera':
        garage_ref = db.collection("Garage")
        garage_doc = garage_ref.document(doc['garageID']).get().to_dict()
        garage_doc['cameraIDs'].append(doc['id'])
        garage_ref.document(doc['garageID']).update(garage_doc)

def special_handlers(collection_ref, db, request, userID):
    validator.validate(db, request.json, collection_ref, is_required=True)

    user_auth.authorize_request(collection_ref, db, request, userID)
    
    if collection_ref == 'Recent':
        return handle_driver_history(db, request.json)
    
    else:
        return handle_add_snaps(db, request.json)

def handle_driver_history(db, doc):
    doc_ref = db.collection('Recent')
    if doc_ref.document(doc['driverID']).get().exists:
        recent_doc = doc_ref.document(doc['driverID']).get().to_dict()
        recent_doc['history'].append({'recent': doc['recent']})
        doc_ref.document(doc['driverID']).update(recent_doc)

    else:
        new_doc = {'driverID': doc['driverID'], 'history': [{'recent': doc['recent']}]}
        doc_ref.document(doc['driverID']).set(new_doc)

    return jsonify(f"Document is added successfully"), 200

def handle_add_snaps(db, doc):
    camera_id = doc['cameraID']
    capacity = doc['capacity']
    path = doc['path']
    mock_garage = doc['mock_garage']
    snap = {'cameraID': camera_id, 'capacity': capacity, 'path': path}
    return user_queries.update_snaps(db, snap, mock_garage)