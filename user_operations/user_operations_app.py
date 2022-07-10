from flask import request, jsonify
from user_operations.HTTP_Exception import HTTP_Exception
import user_operations.user_queries_app as user_queries
import user_operations.user_handlers_app as user_handlers
import user_operations.user_auth_app as user_auth
import user_operations.validator as validator
import datetime as dt


def create(collection_ref, db, userID):
    if collection_ref == 'Recent' or collection_ref == 'Snaps' or  collection_ref == 'GarageSnaps':
        return user_handlers.special_handlers(collection_ref, db, request, userID)
    
    doc_ref = db.collection(collection_ref).document()
    request.json.update({'id': doc_ref.id})

    if collection_ref == "Review":
        request.json.update({'date': dt.datetime.now()})

    validator.validate(db, request.json, collection_ref, is_required=True)

    user_auth.authorize_request(collection_ref, db, request, userID)
    
    user_handlers.handle_add(db, collection_ref, request.json)

    doc_ref.set(request.json)
    return jsonify(f"Document is added successfully"), 200

def get(collection_ref, db):

    doc_ref = db.collection(collection_ref)
    doc_id = request.args.get('id')
    if doc_id:
        if not doc_ref.document(doc_id).get().exists:
            raise HTTP_Exception("document doesn't exit", 404)
        
        doc = doc_ref.document(doc_id).get()
        return jsonify(doc.to_dict()), 200

    else:
        if collection_ref == "Review":
            return user_queries.get_ordered_reviews(db)
        
        all_docs = [doc.to_dict() for doc in doc_ref.stream()]
        return jsonify(all_docs), 200
    
def update(collection_ref, db, userID):
        if collection_ref == 'Recent' or collection_ref == 'Snaps' or  collection_ref == 'GarageSnaps':
            raise HTTP_Exception("Update method is not allowed for this collection", 400)

        doc_ref = db.collection(collection_ref)
        validator.validate(db, request.json, collection_ref, is_required=False)
        doc_id = request.json['id']

        if not doc_ref.document(doc_id).get().exists:    
            raise HTTP_Exception("document doesn't exit", 404)

        user_auth.authorize_request(collection_ref, db, request, userID)
        doc_ref.document(doc_id).update(request.json)
        return jsonify("Document is updated successfully"), 200

def delete(collection_ref, db):
    doc_ref = db.collection(collection_ref)
    doc_id = request.args.get('id')

    if not doc_ref.document(doc_id).get().exists:
        raise HTTP_Exception("document doesn't exit", 404)

    doc = doc_ref.document(doc_id).get()
    user_handlers.handle_delete(db, collection_ref, doc)

    doc_ref.document(doc_id).delete()
    return jsonify("Document is deleted successfully"), 200
