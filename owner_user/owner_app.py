from flask import request, jsonify
import owner_user.validator as validator

def create(db):
    try:
        doc_ref = db.collection('Garages').document()
        request.json.update({'id': doc_ref.id})
        validated, errors = validator.validate(request.json)
        if validated:
            doc_ref.set(request.json)
        else:
            return errors
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
        return f"An Error Occurred: {e}"


def delete(db):
    try:
        garage_ref = db.collection('Garages')
        id = request.json['id']
        garage_ref.document(id).delete()
        return jsonify("Garage is deleted successfully"), 200
    except Exception as e:
        return f"An Error Occurred: {e}"


def show_garage_reviews(db):
    try:
        review_ref = db.collection('Review')
        garage_id = request.json['garageID']
        reviews = review_ref.where('garageID', '==', garage_id).stream()
        result = [review.to_dict() for review in reviews]
        return jsonify(result), 200
    except Exception as e:
        return f"An Error Occurred: {e}"


def show_street_reviews (db):
    try:
        review_ref = db.collection('Review')
        camera_id = request.json['cameraID']
        reviews = review_ref.where('cameraID', '==', camera_id).stream()
        result = [review.to_dict() for review in reviews]
        return jsonify(result), 200
    except Exception as e:
        return f"An Error Occurred: {e}"

def get_owner_garages(db):
    garage_ref = db.collection('Garages')
    try:
        ownerID = request.args.get('ownerID')
        docs = garage_ref.where('ownerID', '==', int(ownerID)).stream()
        response = [doc.to_dict() for doc in docs]
        return jsonify(response), 200
    except Exception as e:
        return f"An Error Occurred: {e}"
    