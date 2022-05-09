from flask import request, jsonify

def create(db):
    garage_ref = db.collection('Garages')
    try:
        id = request.json['id']
        garage_ref.document(id).set(request.json)
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