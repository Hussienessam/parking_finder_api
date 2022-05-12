from flask import request, jsonify
from google.cloud.firestore import GeoPoint
import driver_user.validator as validator

def create(db):
    try:
        bookmark_ref = db.collection('bookmark').document()
        bookmark = {"id": bookmark_ref.id, "name": request.json['name'], "driverID": request.json['driverID'],
                    "location": {'lat': request.json['location']['lat'], 'long': request.json['location']['long']}}
        request.json.update({'id': bookmark_ref.id})
        validated, errors = validator.validate(validator.bookmark_schema, request.json)
        if validated:
            bookmark_ref.set(request.json)
        else: return errors

        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occurred: {e}"


def get(db):
    global key
    bookmark_ref = db.collection('bookmark')
    try:
        bookmark_id = request.args.get('id')
        if bookmark_id:
            result = bookmark_ref.document(bookmark_id).get().to_dict()
            record = {}
            for key in result:
                if isinstance(result[key], GeoPoint):
                    record[key] = str(result[key].latitude) + ',' + str(result[key].longitude)
                    continue
                record[key] = result[key]

                record['key'] = result[key]
            return jsonify(record), 200

        else:
            b = bookmark_ref.stream()
            all = []
            for e in b:
                record = {}
                result = e.to_dict()
                for key in result:
                    if isinstance(result[key], GeoPoint):
                        record[key] = str(result[key].latitude) + ',' + str(result[key].longitude)
                        continue
                    record[key] = result[key]

                    record['key'] = result[key]
                all.append(record)
            return jsonify(all), 200
    except Exception as e:
        return f"An Error Occurred: {e}"


def delete(db):
    bookmark_ref = db.collection('bookmark')
    try:
        bookmark_id = request.json['id']
        bookmark_ref.document(bookmark_id).delete()
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occurred: {e}"