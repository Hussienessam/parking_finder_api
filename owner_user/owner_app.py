import json
from pydoc import doc
from flask import request, jsonify

def create(db):
    try:
        doc_ref = db.collection(u'Garages').document()
        json_request = json.loads(request.data)
        capacity = request.json['capacity'] if 'capacity' in json_request else -1
        garage = {"capacity": capacity, "ownerId": request.json['ownerID'], "id": doc_ref.id}
        doc_ref.set(garage)
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
    garage_ref = db.collection('Garages')
    try:
        id = request.json['id']
        garage_ref.document(id).update(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occurred: {e}"

def delete(db):
    garage_ref = db.collection('Garages')
    try:
        id = request.json['id']
        garage_ref.document(id).delete()
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occurred: {e}"