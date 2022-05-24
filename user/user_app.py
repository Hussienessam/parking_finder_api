from flask import request, jsonify
from firebase_admin import auth
import database.login_connect as db_connection

login_auth = db_connection.connect()


def sign_up(db):
    name = request.args.get('name')
    email = request.args.get('email')
    password = request.args.get('password')
    number = request.args.get('number')
    is_owner = request.args.get('is_owner')
    try:
        user = auth.create_user(email=email,
                                password=password,
                                phone_number=number,
                                display_name=name,
                                )
        doc_ref = db.collection(u'Owner')
        own = {"email": email, "is_owner": is_owner}
        doc_ref.document(user.uid).set(own)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occurred: {e}"


def log_in():
    password = request.args.get('password')
    email = request.args.get('email')
    try:
        user = login_auth.sign_in_with_email_and_password(email, password)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occurred: {e}"


def update_name():
    name = request.args.get('name')
    email = request.args.get('email')
    try:
        user = auth.get_user_by_email(email)
        id = user.uid
        auth.update_user(id, display_name=name)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occurred: {e}"


def update_email():
    email = request.args.get('email')
    new_email = request.args.get('newemail')
    try:
        user = auth.get_user_by_email(email)
        id = user.uid
        auth.update_user(id, email=new_email)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occurred: {e}"


def update_number():
    number = request.args.get('number')
    email = request.args.get('email')
    try:
        user = auth.get_user_by_email(email)
        id = user.uid
        auth.update_user(id, phone_number=number)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occurred: {e}"


def update_password():
    newpass = request.args.get('password')
    email = request.args.get('email')
    try:
        user = auth.get_user_by_email(email)
        id = user.uid
        auth.update_user(id, password=newpass)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occurred: {e}"


def get_by_mail():
    email = request.args.get('email')
    try:
        user = auth.get_user_by_email(email)
        return jsonify({'id': user.uid, 'name': user.display_name, 'email': user.email, 'number': user.phone_number}), 200
    except Exception as e:
        return f"An Error Occurred: {e}"


def get_by_id():
    id = request.args.get('id')
    try:
        user = auth.get_user(id)
        return jsonify({'id': user.uid, 'name': user.display_name, 'email': user.email, 'number': user.phone_number}), 200
    except Exception as e:
        return f"An Error Occurred: {e}"
