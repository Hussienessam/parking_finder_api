from flask import request, jsonify
from firebase_admin import auth
import database.login_connect as db_connection
from flask_jwt_extended import create_access_token

login_auth = db_connection.connect()


def sign_up(db):
    name = request.json['name']
    email = request.json['email']
    password = request.json['password']
    number = request.json['number']
    is_owner = request.json['is_owner']
    try :
        try :
            user = auth.get_user_by_email(email)
            return jsonify({"value": "email already exists"}), 200
        except Exception as e:
            pass
        
        try :
            user = auth.get_user_by_phone_number(number)
            return jsonify({"value": "phone number already exists"}), 200
        except Exception as e:
            pass

        user = auth.create_user(email=email,
                                password=password,
                                phone_number=number,
                                display_name=name,
                                )
        doc_ref = db.collection(u'Owner')
        own = {"email":email, "is_owner":is_owner}
        doc_ref.document(user.uid).set(own)
        return jsonify({"value": "sign in successful"}), 200
    except Exception as e:
        return f"An Error Occurred: {e}"

def get_role(id, db):
    user_ref = db.collection(u'Owner')
    user = user_ref.document(id).get().to_dict()
    if user['is_owner'] == False:
        return "driver"
    else:
        return "owner"

def log_in(db):
    password = request.args.get('password')
    email = request.args.get('email')
    try:
        try :
            user = login_auth.sign_in_with_email_and_password(email, password)
            return jsonify({"value": "incorrect email or password"}), 200
        except Exception as e:
            pass

        access_token = create_access_token(identity=get_role(user['localId'], db))
        return jsonify(
            {'id': user['localId'], 'idToken': access_token, 'value': "login successful"}), 200
    except Exception as e:
        return f"An Error Occurred: {e}"


def update_name():
    name = request.json['name']
    email = request.json['email']
    try:
        user = auth.get_user_by_email(email)
        id = user.uid
        auth.update_user(id, display_name=name)
        user = auth.get_user(id)
        return jsonify(
            {'id': user.uid, 'name': user.display_name, 'email': user.email, 'number': user.phone_number}), 200

    except Exception as e:
        return f"An Error Occurred: {e}"


def update_email():
    email = request.json['email']
    new_email = request.json['newemail']
    try:
        user = auth.get_user_by_email(email)
        id = user.uid
        auth.update_user(id, email=new_email)
        user = auth.get_user(id)
        return jsonify(
            {'id': user.uid, 'name': user.display_name, 'email': user.email, 'number': user.phone_number}), 200

    except Exception as e:
        return f"An Error Occurred: {e}"


def update_number():
    number = request.json['number']
    email = request.json['email']
    try:
        user = auth.get_user_by_email(email)
        id = user.uid
        auth.update_user(id, phone_number=number)
        user = auth.get_user(id)
        return jsonify(
            {'id': user.uid, 'name': user.display_name, 'email': user.email, 'number': user.phone_number}), 200

    except Exception as e:
        return f"An Error Occurred: {e}"


def update_password():
    newpass = request.json['password']
    email = request.json['email']
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


def get_by_id_for_garage(id):
    try:
        user = auth.get_user(id)
        return {'id': user.uid, 'name': user.display_name, 'email': user.email, 'number': user.phone_number}
    except Exception as e:
        return f"An Error Occurred: {e}"
