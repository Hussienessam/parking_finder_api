from flask import request, jsonify
import driver_user.validator as validator


def create(db):
    try:
        bookmark_ref = db.collection('bookmark').document()
        bookmark = {"id": bookmark_ref.id, "name": request.json['name'], "driverID": request.json['driverID'],
                    "location": {'lat': request.json['location']['lat'], 'long': request.json['location']['long']}}
        validated, errors = validator.validate(
            validator.bookmark_schema, bookmark)
        if validated:
            bookmark_ref.set(bookmark)
        else:
            return errors

        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occurred: {e}"


def get(db):
    bookmark_ref = db.collection('bookmark')
    try:
        if request.json:
            bookmark_id = request.json['id']
            if bookmark_id:
                if bookmark_ref.document(bookmark_id).get().exists:
                    bookmark = bookmark_ref.document(bookmark_id).get()
                    return jsonify(bookmark.to_dict()), 200
                else:
                    return "document doesn't exist"
        else:
            all_bookmarks = [doc.to_dict() for doc in bookmark_ref.stream()]
            return jsonify(all_bookmarks), 200

    except Exception as e:
        return f"An Error Occurred: {e}"


def delete(db):
    bookmark_ref = db.collection('bookmark')
    try:
        bookmark_id = request.json['id']
        if bookmark_ref.document(bookmark_id).get().exists:
            bookmark_ref.document(bookmark_id).delete()
            return jsonify({"success": True}), 200
        else:
            return "document doesn't exist"
    except Exception as e:
        return f"An Error Occurred: {e}"
