import imp
import json
from pydoc import doc
from flask import request, jsonify
import owner_user.validator as v

def create(db):
    try:
        doc_ref = db.collection(u'Garages').document()
        # garage = {"capacity": capacity, "ownerId": request.json['ownerID'], "id": doc_ref.id}
        request.json.update({'id': doc_ref.id})
        doc_ref.set(request.json)
        # v.validate(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occurred: {e}"

def get(db):
    garage_ref = db.collection('Garages')
    try:
        garage_id = request.args.get('id')
        if garage_id:
            garage = garage_ref.document(garage_id).get()
            return jsonify(garage.to_dict()), 200
        else:
            all_garages = [doc.to_dict() for doc in garage_ref.stream()]
            return jsonify(all_garages), 200
    except Exception as e:
        return f"An Error Occurred: {e}"


def update(db):
    try:
        garage_ref = db.collection('Garages')
        id = request.json['id']
        garage_ref.document(id).update(request.json)
        return jsonify("Garage is updated successfully"), 200
    except Exception as e:
        return jsonify("ID is required"), 500


def delete(db):
    try:
        garage_ref = db.collection('Garages')
        id = request.json['id']
        garage_ref.document(id).delete()
        return jsonify("Garage is deleted successfully"), 200
    except Exception as e:
        return jsonify("ID is required"), 500


def show_reviews_garage(db):
    try:
        review_ref = db.collection('Review')
        garage_id = request.json['garageID']
        reviews = review_ref.where(u'garageID', u'==', garage_id).stream()
        result = [review.to_dict() for review in reviews]
        return jsonify(result), 200
    except Exception as e:
        return jsonify("garageID is required"), 500


def show_reviews_street(db):
    try:
        review_ref = db.collection('Review')
        camera_id = request.json['cameraID']
        reviews = review_ref.where(u'cameraID', u'==', camera_id).stream()
        result = [review.to_dict() for review in reviews]
        return jsonify(result), 200
    except Exception as e:
        return jsonify("cameraID is required"), 500