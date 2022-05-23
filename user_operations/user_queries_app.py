from flask import request, jsonify

def show_garage_reviews(db):
    try:
        review_ref = db.collection('Review')
        garage_id = request.json['garageID']
        reviews = review_ref.where('garageID', '==', garage_id).stream()
        result = [review.to_dict() for review in reviews]
        return jsonify(result), 200
    except Exception as e:
        return f"An Error Occurred: {e}"


def show_street_reviews(db):
    try:
        review_ref = db.collection('Review')
        camera_id = request.json['cameraID']
        reviews = review_ref.where('cameraID', '==', camera_id).stream()
        result = [review.to_dict() for review in reviews]
        return jsonify(result), 200
    except Exception as e:
        return f"An Error Occurred: {e}"


def get_owner_garages(db):
    try:
        garage_ref = db.collection('Garage')
        ownerID = request.json['ownerID']
        docs = garage_ref.where('ownerID', '==', ownerID).stream()
        response = [doc.to_dict() for doc in docs]
        return jsonify(response), 200
    except Exception as e:
        return f"An Error Occurred: {e}"

def get_user_bookmark(db):
    try:
        bookmark_ref = db.collection('Bookmark')
        driverID = request.args.get('driverID')
        docs = bookmark_ref.where('driverID', '==', driverID).stream()
        response = [doc.to_dict() for doc in docs]
        return jsonify(response), 200
    except Exception as e:
        return f"An Error Occurred: {e}"