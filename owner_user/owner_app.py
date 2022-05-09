from flask import Flask, request, jsonify

import database.connect_database as db

db.connect()

# app = Flask(__name__)@app.route('/add', methods=['POST'])

# def create():
#     """
#         create() : Add document to Firestore collection with request body.
#         Ensure you pass a custom ID as part of json body in post request,
#         e.g. json={'id': '1', 'title': 'Write a blog post'}
#     """
#     try:
#         id = request.json['id']
#         todo_ref.document(id).set(request.json)
#         return jsonify({"success": True}), 200
#     except Exception as e:
#         return f"An Error Occurred: {e}"

# @app.route('/list', methods=['GET'])
# def read():
#     """
#         read() : Fetches documents from Firestore collection as JSON.
#         todo : Return document that matches query ID.
#         all_todos : Return all documents.
#     """
#     try:
#         # Check if ID was passed to URL query
#         todo_id = request.args.get('id')
#         if todo_id:
#             todo = todo_ref.document(todo_id).get()
#             return jsonify(todo.to_dict()), 200
#         else:
#             all_todos = [doc.to_dict() for doc in todo_ref.stream()]
#             return jsonify(all_todos), 200
#     except Exception as e:
#         return f"An Error Occurred: {e}"