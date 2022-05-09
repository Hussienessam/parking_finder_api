from flask import request, jsonify

def create(db):
    garage_ref = db.collection('Garages')
    try:
        id = request.json['id']
        garage_ref.document(id).set(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occurred: {e}"