from flask import request, jsonify
import datetime as dt
import driver_user.validator as validator
def create(db):
    try:
        review_ref = db.collection(u'Review').document()
        review = {"id": review_ref.id, "content": request.json['content'], "date": dt.datetime.now(),
                  "cameraID": request.json['cameraID'], "driverID": request.json['driverID'],
                  "garageID": request.json['garageID']}
        validated, errors = validator.validate(validator.review_schema, review)
        if validated:
            review_ref.set(review)
        else: return errors
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occurred: {e}"


def get(db):
    review_ref = db.collection('Review')
    try:
        review_id = request.args.get('id')
        if review_id:
            review = review_ref.document(review_id).get()
            return jsonify(review.to_dict()), 200
        else:
            all_reviews = [doc.to_dict() for doc in review_ref.stream()]
            return jsonify(all_reviews), 200
    except Exception as e:
        return f"An Error Occurred: {e}"


def delete(db):
    review_ref = db.collection('Review')
    try:
        review_id = request.json['id']
        review_ref.document(review_id).delete()
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occurred: {e}"