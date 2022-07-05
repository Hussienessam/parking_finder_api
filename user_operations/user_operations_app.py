from flask import request, jsonify
import user_operations.user_queries_app as user_queries
import user_operations.validator as validator
import datetime as dt


def create(collection_ref, db):
    try:
        doc_ref = db.collection(collection_ref).document()
        request.json.update({'id': doc_ref.id})

        if collection_ref == "Review":
            request.json.update({'date': dt.datetime.now()})

        validated, errors = validator.validate(db,
            request.json, collection_ref, is_required=True)

        if validated:
            user_queries.handle_add(db, collection_ref, request.json)
            doc_ref.set(request.json)
            return jsonify(f"Document is added successfully"), 200

        else:
            return errors, 400
    
    except Exception as e:
        return f"An Error Occurred: {e}", 400


def get(collection_ref, db):
    try:
        doc_ref = db.collection(collection_ref)
        doc_id = request.args.get('id')
        if doc_id:
            if doc_ref.document(doc_id).get().exists:
                doc = doc_ref.document(doc_id).get()
                return jsonify(doc.to_dict()), 200

            else:
                return "document doesn't exist", 404
        else:
            if collection_ref == "Review":
                all_docs = user_queries.get_ordered_reviews(db)
                return jsonify(all_docs), 200
            all_docs = [doc.to_dict() for doc in doc_ref.stream()]
            return jsonify(all_docs), 200
    
    except Exception as e:
        return f"An Error Occurred: {e}", 400


def get_camera(id,db):
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

def update(collection_ref, db):
    try:
        doc_ref = db.collection(collection_ref)
        validated, errors = validator.validate(db,
            request.json, collection_ref, is_required=False)

        if validated:
            doc_id = request.json['id']

            if doc_ref.document(doc_id).get().exists:
                doc_ref.document(doc_id).update(request.json)
                return jsonify("Document is updated successfully"), 200

            else:
                return "document doesn't exist", 404
        
        else:
            return errors, 400
    
    except Exception as e:
        return f"An Error Occurred: {e}", 404


def delete(collection_ref, db):
    try:
        doc_ref = db.collection(collection_ref)
        doc_id = request.args.get('id')

        if doc_ref.document(doc_id).get().exists:
            doc =  doc_ref.document(doc_id).get()
            user_queries.handle_delete(db, collection_ref, doc)
            doc_ref.document(doc_id).delete()
            return jsonify("Document is deleted successfully"), 200

        else:
            return "document doesn't exist", 404
    
    except Exception as e:
        return f"An Error Occurred: {e}", 400
